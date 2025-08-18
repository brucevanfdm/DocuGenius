import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { ConfigurationManager } from './configuration';
import { StatusManager } from './statusManager';

const execAsync = promisify(exec);

export interface ConversionResult {
    success: boolean;
    outputPath?: string;
    error?: string;
}

export class MarkitdownConverter {
    private context: vscode.ExtensionContext;
    private configManager: ConfigurationManager;
    private statusManager: StatusManager;
    private isBatchMode: boolean = false;

    constructor(context: vscode.ExtensionContext, configManager: ConfigurationManager, statusManager: StatusManager) {
        this.context = context;
        this.configManager = configManager;
        this.statusManager = statusManager;
    }

    /**
     * Process a file (convert or copy based on type)
     */
    async processFile(filePath: string, forceConvert: boolean = false, isBatchMode: boolean = false): Promise<ConversionResult> {
        this.isBatchMode = isBatchMode;
        // CRITICAL: Prevent infinite loop - never process files in markdown directory
        const markdownSubdirName = this.configManager.getMarkdownSubdirectoryName();
        if (filePath.includes(`/${markdownSubdirName}/`) || filePath.includes(`\\${markdownSubdirName}\\`)) {
            console.log(`LOOP PREVENTION: Ignoring file in markdown directory: ${filePath}`);
            return { success: true, outputPath: filePath };
        }

        const fileExtension = path.extname(filePath).toLowerCase();
        const supportedExtensions = this.configManager.getSupportedExtensions();

        if (supportedExtensions.includes(fileExtension)) {
            // Convert document files
            return this.convertFile(filePath, forceConvert);
        } else if (this.configManager.shouldCopyTextFiles()) {
            // Copy text-based files only if user has enabled this option
            return this.copyFile(filePath, forceConvert);
        } else {
            // Skip processing if text file copying is disabled
            console.log(`Skipping text file (copying disabled): ${filePath}`);
            return { success: true, outputPath: filePath };
        }
    }

    /**
     * Convert a single file to Markdown
     */
    async convertFile(filePath: string, forceConvert: boolean = false): Promise<ConversionResult> {
        try {
            // Check if file exists
            if (!fs.existsSync(filePath)) {
                throw new Error(`File not found: ${filePath}`);
            }

            // Check if conversion is needed (file modification time) - skip if forced
            const outputPath = this.getOutputPath(filePath);
            if (!forceConvert && !this.shouldConvert(filePath, outputPath)) {
                console.log(`Skipping conversion for ${filePath} - output is up to date`);
                return { success: true, outputPath };
            }

            // Show progress
            const fileName = path.basename(filePath);
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: `Converting ${fileName} to Markdown...`,
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 0 });
                
                try {
                    // Convert using built-in conversion engine
                    const markdownContent = await this.callConverter(filePath);
                    
                    progress.report({ increment: 50 });
                    
                    // Save the markdown file
                    fs.writeFileSync(outputPath, markdownContent, 'utf8');
                    
                    progress.report({ increment: 100 });
                    
                    // Show success message with action buttons (if enabled and not in batch mode)
                    if (this.configManager.shouldShowSuccessNotifications() && !this.isBatchMode) {
                        vscode.window.showInformationMessage(
                            `Successfully converted ${fileName}`,
                            'Open File',
                            'Open Folder'
                        ).then(selection => {
                            if (selection === 'Open File') {
                                // Open the converted file
                                vscode.workspace.openTextDocument(outputPath).then(doc => {
                                    vscode.window.showTextDocument(doc);
                                });
                            } else if (selection === 'Open Folder') {
                                // Open the containing folder in VS Code
                                const folderUri = vscode.Uri.file(path.dirname(outputPath));
                                vscode.commands.executeCommand('vscode.openFolder', folderUri, { forceNewWindow: false });
                            }
                        });
                    }
                    
                } catch (error) {
                    console.error(`Error converting ${filePath}:`, error);
                    vscode.window.showErrorMessage(
                        `Failed to convert ${fileName}: ${error instanceof Error ? error.message : 'Unknown error'}`
                    );
                    throw error;
                }
            });

            return { success: true, outputPath };

        } catch (error) {
            console.error(`Error converting file ${filePath}:`, error);
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }

    /**
     * Process all supported files in a folder
     */
    async convertFolder(folderPath: string): Promise<ConversionResult[]> {
        try {
            // Find all processable files (both convertible and copyable)
            const allExtensions = [
                ...this.configManager.getSupportedExtensions(),
                '.md', '.markdown', '.mdown', '.mkd', '.mkdn',
                '.txt', '.text',
                '.json', '.jsonc',
                '.xml', '.html', '.htm',
                '.csv', '.tsv',
                '.log',
                '.yaml', '.yml',
                '.toml', '.ini', '.cfg', '.conf',
                '.sql'
            ];

            const files = this.findSupportedFiles(folderPath, allExtensions);

            if (files.length === 0) {
                vscode.window.showInformationMessage('No processable files found in the selected folder.');
                return [];
            }

            const results: ConversionResult[] = [];
            
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: `Converting ${files.length} files...`,
                cancellable: false
            }, async (progress) => {
                const increment = 100 / files.length;
                
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    progress.report({
                        increment: i === 0 ? 0 : increment,
                        message: `Processing ${path.basename(file)}...`
                    });

                    const result = await this.processFile(file, false, true); // Enable batch mode
                    results.push(result);
                }
                
                progress.report({ increment: 100 });
            });

            const successCount = results.filter(r => r.success).length;
            const failureCount = results.length - successCount;
            
            if (failureCount === 0) {
                if (this.configManager.shouldShowSuccessNotifications()) {
                    vscode.window.showInformationMessage(
                        `Successfully processed ${successCount} files!`,
                        'Open Output Folder',
                        'Show Details'
                    ).then(selection => {
                        if (selection === 'Open Output Folder') {
                            // Open the kb folder
                            const kbFolder = path.join(folderPath, this.configManager.getMarkdownSubdirectoryName());
                            if (fs.existsSync(kbFolder)) {
                                vscode.commands.executeCommand('revealFileInOS', vscode.Uri.file(kbFolder));
                            }
                        } else if (selection === 'Show Details') {
                            // Show output panel with conversion details
                            vscode.commands.executeCommand('workbench.action.output.toggleOutput');
                        }
                    });
                }
            } else {
                // Always show warnings, even if success notifications are disabled
                vscode.window.showWarningMessage(
                    `⚠️ Processed ${successCount} files successfully, ${failureCount} failed.`,
                    'Show Details',
                    'Open Output Folder'
                ).then(selection => {
                    if (selection === 'Show Details') {
                        vscode.commands.executeCommand('workbench.action.output.toggleOutput');
                    } else if (selection === 'Open Output Folder') {
                        const kbFolder = path.join(folderPath, this.configManager.getMarkdownSubdirectoryName());
                        if (fs.existsSync(kbFolder)) {
                            vscode.commands.executeCommand('revealFileInOS', vscode.Uri.file(kbFolder));
                        }
                    }
                });
            }

            return results;

        } catch (error) {
            console.error(`Error converting folder ${folderPath}:`, error);
            vscode.window.showErrorMessage(`Failed to convert folder: ${error instanceof Error ? error.message : 'Unknown error'}`);
            return [];
        }
    }

    /**
     * Call built-in converter to convert file
     */
    private async callConverter(filePath: string): Promise<string> {
        try {
            // Try embedded binary first, then fallback to system installations
            const commands = this.getConverterCommands();

            let lastError: Error | null = null;

            for (const command of commands) {
                try {
                    const fullCommand = `"${command}" "${filePath}"`;
                    const { stdout, stderr } = await execAsync(fullCommand);

                    if (stderr && !stdout) {
                        throw new Error(`Converter error: ${stderr}`);
                    }

                    // Process the markdown content to handle images if needed
                    let markdownContent = stdout;

                    if (this.configManager.shouldExtractImages()) {
                        markdownContent = await this.processImages(filePath, markdownContent);
                    }

                    return markdownContent;

                } catch (error) {
                    lastError = error instanceof Error ? error : new Error(String(error));
                    continue; // Try next command
                }
            }

            // If all commands failed, throw helpful error
            const hasEmbeddedBinary = fs.existsSync(this.context.asAbsolutePath(`bin/${process.platform}/docugenius-cli${process.platform === 'win32' ? '.bat' : ''}`));

            if (hasEmbeddedBinary) {
                throw new Error(
                    `Embedded converter binary failed to execute. This might be due to:\n\n` +
                    `1. Missing system libraries\n` +
                    `2. Architecture mismatch\n` +
                    `3. Permission issues\n\n` +
                    `Last error: ${lastError?.message || 'Unknown error'}`
                );
            } else {
                throw new Error(
                    `Built-in converter is not available. Please check the extension installation.\n\n` +
                    `Last error: ${lastError?.message || 'Unknown error'}`
                );
            }

        } catch (error) {
            throw error;
        }
    }



    /**
     * Get output path for converted/copied file
     */
    private getOutputPath(filePath: string): string {
        const dir = path.dirname(filePath);
        const fileName = path.basename(filePath);
        const fileExtension = path.extname(filePath).toLowerCase();

        if (this.configManager.shouldOrganizeInSubdirectory()) {
            // Create a subdirectory for processed files
            const subdirName = this.configManager.getMarkdownSubdirectoryName();
            const markdownDir = path.join(dir, subdirName);

            // Ensure the markdown directory exists
            if (!fs.existsSync(markdownDir)) {
                fs.mkdirSync(markdownDir, { recursive: true });
            }

            // For files that need conversion, use .md extension
            const supportedExtensions = this.configManager.getSupportedExtensions();
            if (supportedExtensions.includes(fileExtension)) {
                const nameWithoutExt = path.parse(fileName).name;
                return path.join(markdownDir, `${nameWithoutExt}.md`);
            } else {
                // For files that are just copied, keep original extension
                return path.join(markdownDir, fileName);
            }
        } else {
            // Keep files in the same directory
            const supportedExtensions = this.configManager.getSupportedExtensions();
            if (supportedExtensions.includes(fileExtension)) {
                const nameWithoutExt = path.parse(fileName).name;
                return path.join(dir, `${nameWithoutExt}.md`);
            } else {
                // For copied files, add a suffix to avoid conflicts
                const nameWithoutExt = path.parse(fileName).name;
                const ext = path.parse(fileName).ext;
                return path.join(dir, `${nameWithoutExt}_copy${ext}`);
            }
        }
    }

    /**
     * Check if conversion is needed
     */
    private shouldConvert(inputPath: string, outputPath: string): boolean {
        // If output doesn't exist, convert
        if (!fs.existsSync(outputPath)) {
            return true;
        }

        // If overwrite is disabled, skip
        if (!this.configManager.shouldOverwriteExisting()) {
            return false;
        }

        // Check modification times
        const inputStat = fs.statSync(inputPath);
        const outputStat = fs.statSync(outputPath);
        
        return inputStat.mtime > outputStat.mtime;
    }

    /**
     * Find all supported files in a directory
     */
    private findSupportedFiles(dirPath: string, supportedExtensions: string[]): string[] {
        const files: string[] = [];
        
        const scanDirectory = (currentPath: string) => {
            const items = fs.readdirSync(currentPath);
            
            for (const item of items) {
                const itemPath = path.join(currentPath, item);
                const stat = fs.statSync(itemPath);
                
                if (stat.isDirectory()) {
                    scanDirectory(itemPath);
                } else if (stat.isFile()) {
                    // Skip DocuGenius configuration files
                    if (item === '.docugenius.json' || item === '.docugenius.example.json') {
                        continue;
                    }
                    
                    const ext = path.extname(item).toLowerCase();
                    if (supportedExtensions.includes(ext)) {
                        files.push(itemPath);
                    }
                }
            }
        };
        
        scanDirectory(dirPath);
        return files;
    }

    /**
     * Get available converter commands in order of preference
     */
    private getConverterCommands(): string[] {
        const platform = process.platform;
        const commands: string[] = [];

        // 1. Try embedded binary first
        const binaryName = platform === 'win32' ? 'docugenius-cli.bat' : 'docugenius-cli';
        const embeddedBinaryPath = this.context.asAbsolutePath(`bin/${platform}/${binaryName}`);

        // Check if embedded binary exists
        if (fs.existsSync(embeddedBinaryPath)) {
            commands.push(embeddedBinaryPath);
        }

        return commands;
    }

    /**
     * Copy a text-based file to the markdown directory
     */
    async copyFile(filePath: string, forceConvert: boolean = false): Promise<ConversionResult> {
        try {
            // Check if file exists
            if (!fs.existsSync(filePath)) {
                throw new Error(`File not found: ${filePath}`);
            }

            const outputPath = this.getOutputPath(filePath);

            // Check if copy is needed (file modification time) - skip if forced
            if (!forceConvert && !this.shouldConvert(filePath, outputPath)) {
                console.log(`Skipping copy for ${filePath} - output is up to date`);
                return { success: true, outputPath };
            }

            // Show progress
            const fileName = path.basename(filePath);
            this.statusManager.showConversionInProgress(fileName);

            // Copy the file
            const fileContent = fs.readFileSync(filePath, 'utf8');
            fs.writeFileSync(outputPath, fileContent, 'utf8');

            // Show success message (suppress notification in batch mode)
            this.statusManager.showConversionSuccess(filePath, outputPath, this.isBatchMode);
            this.statusManager.log(`✓ Copied: ${fileName} → ${path.basename(outputPath)}`);

            return { success: true, outputPath };

        } catch (error) {
            console.error(`Error copying file ${filePath}:`, error);
            const fileName = path.basename(filePath);
            this.statusManager.showConversionError(fileName, error instanceof Error ? error.message : 'Unknown error');
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }

    /**
     * Handle file deletion - clean up corresponding markdown file and assets
     */
    async handleFileDeleted(filePath: string): Promise<void> {
        try {
            const fileName = path.basename(filePath);
            console.log(`Handling deletion of: ${fileName}`);

            // Get the corresponding output path
            const outputPath = this.getOutputPath(filePath);

            // Delete the markdown file if it exists
            if (fs.existsSync(outputPath)) {
                fs.unlinkSync(outputPath);
                console.log(`Deleted corresponding markdown file: ${outputPath}`);
                this.statusManager.log(`🗑️ Deleted: ${path.basename(outputPath)} (source file ${fileName} was deleted)`);
            }

            // Delete assets folder if it exists
            const originalDir = path.dirname(filePath);
            const originalBaseName = path.parse(fileName).name;

            let assetsDir: string;
            if (this.configManager.shouldOrganizeInSubdirectory()) {
                const subdirName = this.configManager.getMarkdownSubdirectoryName();
                const markdownDir = path.join(originalDir, subdirName);
                assetsDir = path.join(markdownDir, `${originalBaseName}_assets`);
            } else {
                assetsDir = path.join(originalDir, `${originalBaseName}_assets`);
            }

            if (fs.existsSync(assetsDir)) {
                fs.rmSync(assetsDir, { recursive: true, force: true });
                console.log(`Deleted assets folder: ${assetsDir}`);
                this.statusManager.log(`🗑️ Deleted assets: ${originalBaseName}_assets/`);
            }

            // Show status update
            this.statusManager.updateStatusBar(`🗑️ Cleaned up ${fileName}`, `Deleted markdown file and assets for ${fileName}`);

            // Reset status bar after 3 seconds
            setTimeout(() => {
                this.statusManager.updateStatusBar('Ready');
            }, 3000);

        } catch (error) {
            console.error(`Error handling file deletion for ${filePath}:`, error);
            this.statusManager.log(`❌ Error cleaning up deleted file ${path.basename(filePath)}: ${error}`);
        }
    }

    /**
     * Check if a file should be converted to Markdown
     */
    private shouldFileBeConverted(filePath: string): boolean {
        const fileExtension = path.extname(filePath).toLowerCase();

        // Skip files that VS Code already handles well
        const vscodeNativeFormats = [
            '.md', '.markdown', '.mdown', '.mkd', '.mkdn',  // Markdown files
            '.txt', '.text',                                // Plain text files
            '.json', '.jsonc',                             // JSON files
            '.xml', '.html', '.htm',                       // Markup files
            '.csv', '.tsv',                                // Simple data files
            '.log',                                        // Log files
            '.yaml', '.yml',                               // YAML files
            '.toml', '.ini', '.cfg', '.conf',             // Config files
            '.js', '.ts', '.jsx', '.tsx',                 // Code files
            '.py', '.java', '.cpp', '.c', '.h',           // More code files
            '.css', '.scss', '.sass', '.less',            // Style files
            '.sql',                                        // SQL files
        ];

        if (vscodeNativeFormats.includes(fileExtension)) {
            return false;
        }

        // Only convert supported document formats
        const supportedExtensions = this.configManager.getSupportedExtensions();
        return supportedExtensions.includes(fileExtension);
    }

    /**
     * Get the reason why a file is being skipped
     */
    private getSkipReason(filePath: string): string {
        const fileExtension = path.extname(filePath).toLowerCase();

        const vscodeNativeFormats = [
            '.md', '.markdown', '.mdown', '.mkd', '.mkdn',
            '.txt', '.text',
            '.json', '.jsonc',
            '.xml', '.html', '.htm',
            '.csv', '.tsv',
            '.log',
            '.yaml', '.yml',
            '.toml', '.ini', '.cfg', '.conf',
            '.js', '.ts', '.jsx', '.tsx',
            '.py', '.java', '.cpp', '.c', '.h',
            '.css', '.scss', '.sass', '.less',
            '.sql',
        ];

        if (vscodeNativeFormats.includes(fileExtension)) {
            return 'VS Code already supports this format natively';
        }

        const supportedExtensions = this.configManager.getSupportedExtensions();
        if (!supportedExtensions.includes(fileExtension)) {
            return `Unsupported format (supported: ${supportedExtensions.join(', ')})`;
        }

        return 'Unknown reason';
    }

    /**
     * Enhanced image processing with actual image extraction
     */
    private async processImages(originalFilePath: string, markdownContent: string): Promise<string> {
        try {
            const originalDir = path.dirname(originalFilePath);
            const originalBaseName = path.parse(path.basename(originalFilePath)).name;
            const fileExtension = path.extname(originalFilePath).toLowerCase();

            // Check if image extraction is enabled
            if (!this.configManager.shouldExtractImages()) {
                // If image extraction is disabled, just process existing image references
                return this.processExistingImageReferences(originalFilePath, markdownContent);
            }

            // Only extract images from supported document types
            if (!['.pdf', '.docx', '.pptx', '.xlsx'].includes(fileExtension)) {
                // For other files, just process existing image references
                return this.processExistingImageReferences(originalFilePath, markdownContent);
            }

            // Try to extract images using the image extractor
            let extractedImages: any[] = [];
            let imageExtractionResult: any = null;

            try {
                imageExtractionResult = await this.extractImagesFromDocument(originalFilePath);
                if (imageExtractionResult && imageExtractionResult.success) {
                    extractedImages = imageExtractionResult.images || [];
                }
            } catch (error) {
                console.warn(`Warning: Image extraction failed for ${originalFilePath}:`, error);
                // Continue with processing existing references
            }

            // Check if we have intelligent extraction result with full content
            if (imageExtractionResult && imageExtractionResult.success && imageExtractionResult.markdown_content) {
                // Use the intelligent extraction result that has images in original positions
                let intelligentContent = imageExtractionResult.markdown_content;

                // Process any existing image references in the intelligent content
                intelligentContent = await this.processExistingImageReferences(originalFilePath, intelligentContent);

                return intelligentContent;
            } else {
                // Fallback to traditional processing
                let processedContent = await this.processExistingImageReferences(originalFilePath, markdownContent);

                // Add extracted images to markdown content if any were found
                if (extractedImages.length > 0) {
                    processedContent += this.generateImageMarkdown(extractedImages);

                    // Add metadata comment
                    processedContent += `\n\n<!-- Images extracted: ${extractedImages.length} images saved to ${imageExtractionResult.output_dir} -->\n`;
                }

                return processedContent;
            }

        } catch (error) {
            console.warn(`Warning: Could not process images for ${originalFilePath}:`, error);
            return markdownContent; // Return original content if image processing fails
        }
    }

    /**
     * Extract images from document using the Python image extractor
     */
    private async extractImagesFromDocument(filePath: string): Promise<any> {
        try {
            const platform = process.platform;
            const imageExtractorPath = this.context.asAbsolutePath(`bin/${platform}/image_extractor.py`);

            // Check if image extractor exists
            if (!fs.existsSync(imageExtractorPath)) {
                console.warn(`Image extractor not found at: ${imageExtractorPath}`);
                return null;
            }

            // Determine output directory based on configuration
            const originalDir = path.dirname(filePath);
            const imageOutputFolder = this.configManager.getImageOutputFolder();
            let outputDir: string;
            let markdownDir: string;

            if (this.configManager.shouldOrganizeInSubdirectory()) {
                const subdirName = this.configManager.getMarkdownSubdirectoryName();
                markdownDir = path.join(originalDir, subdirName);
                outputDir = path.join(markdownDir, imageOutputFolder);
            } else {
                markdownDir = originalDir;
                outputDir = path.join(originalDir, imageOutputFolder);
            }

            // Get minimum image size from configuration
            const minImageSize = this.configManager.getImageMinSize();

            // Call the intelligent image extractor with full content extraction
            const command = `python "${imageExtractorPath}" "${filePath}" "${outputDir}" "${outputDir}" full_content ${minImageSize}`;
            const { stdout, stderr } = await execAsync(command);

            if (stderr && !stdout) {
                throw new Error(`Image extractor error: ${stderr}`);
            }

            // Parse JSON result
            const result = JSON.parse(stdout);
            return result;

        } catch (error) {
            console.warn(`Warning: Failed to extract images from ${filePath}:`, error);
            return null;
        }
    }

    /**
     * Process existing image references in markdown content (legacy functionality)
     */
    private async processExistingImageReferences(originalFilePath: string, markdownContent: string): Promise<string> {
        try {
            const originalDir = path.dirname(originalFilePath);
            const originalBaseName = path.parse(path.basename(originalFilePath)).name;

            // First check if there are any images in the markdown content
            const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
            const hasImages = imageRegex.test(markdownContent);

            if (!hasImages) {
                // No images found, return content as-is without creating assets folder
                return markdownContent;
            }

            let assetsDir: string;

            if (this.configManager.shouldOrganizeInSubdirectory()) {
                // Create assets directory in the kb subdirectory
                const subdirName = this.configManager.getMarkdownSubdirectoryName();
                const markdownDir = path.join(originalDir, subdirName);
                assetsDir = path.join(markdownDir, `${originalBaseName}_assets`);
            } else {
                // Create assets directory in the same location as the original file
                assetsDir = path.join(originalDir, `${originalBaseName}_assets`);
            }

            // Create assets directory only when we have images
            if (!fs.existsSync(assetsDir)) {
                fs.mkdirSync(assetsDir, { recursive: true });
            }

            // Process image references in markdown
            // Reset regex for processing (reuse the same regex variable)
            imageRegex.lastIndex = 0; // Reset regex state
            let processedContent = markdownContent;
            let match;

            while ((match = imageRegex.exec(markdownContent)) !== null) {
                const [fullMatch, altText, imagePath] = match;

                // If image path is not already relative to assets folder, update it
                if (!imagePath.startsWith(`${originalBaseName}_assets/`)) {
                    const imageName = path.basename(imagePath);
                    const newImagePath = `${originalBaseName}_assets/${imageName}`;
                    processedContent = processedContent.replace(fullMatch, `![${altText}](${newImagePath})`);
                }
            }

            return processedContent;

        } catch (error) {
            console.warn(`Warning: Could not process existing image references for ${originalFilePath}:`, error);
            return markdownContent;
        }
    }

    /**
     * Generate markdown content for extracted images
     */
    private generateImageMarkdown(images: any[]): string {
        if (!images || images.length === 0) {
            return "";
        }

        let markdown = "\n\n## Extracted Images\n\n";

        for (const img of images) {
            let altText = "Extracted image";
            if (img.page) {
                altText += ` from page ${img.page}`;
            } else if (img.slide) {
                altText += ` from slide ${img.slide}`;
            }

            // Use relative path for markdown
            markdown += `![${altText}](${img.relative_path})\n\n`;
        }

        return markdown;
    }
}
