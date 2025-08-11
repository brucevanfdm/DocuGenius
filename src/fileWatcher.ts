import * as vscode from 'vscode';
import * as path from 'path';
import { MarkitdownConverter } from './converter';
import { ConfigurationManager } from './configuration';
import { StatusManager } from './statusManager';

export class FileWatcher implements vscode.Disposable {
    private watchers: vscode.FileSystemWatcher[] = [];
    private converter: MarkitdownConverter;
    private configManager: ConfigurationManager;
    private statusManager: StatusManager;

    constructor(converter: MarkitdownConverter, configManager: ConfigurationManager, statusManager: StatusManager) {
        this.converter = converter;
        this.configManager = configManager;
        this.statusManager = statusManager;
        this.initializeWatchers();

        // Listen for configuration changes
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('documentConverter')) {
                this.reinitializeWatchers();
            }
        });
    }

    private initializeWatchers(): void {
        // Dispose existing watchers
        this.disposeWatchers();

        // Only create watchers if auto-convert is enabled
        if (!this.configManager.isAutoConvertEnabled()) {
            return;
        }

        // Get all extensions we want to monitor (both convertible and copyable)
        const convertibleExtensions = this.configManager.getSupportedExtensions();
        const copyableExtensions = [
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

        const allExtensions = [...convertibleExtensions, ...copyableExtensions];

        // Create a pattern for all supported extensions, but exclude markdown directory
        const extensionPattern = allExtensions.map(ext => ext.replace('.', '')).join(',');
        const markdownSubdirName = this.configManager.getMarkdownSubdirectoryName();
        const pattern = `**/*.{${extensionPattern}}`;

        console.log(`Creating file watcher for pattern: ${pattern}`);
        console.log(`Excluding markdown directory: ${markdownSubdirName}`);

        const watcher = vscode.workspace.createFileSystemWatcher(pattern);

        // Handle file creation
        watcher.onDidCreate(async (uri) => {
            console.log(`File created: ${uri.fsPath}`);
            await this.handleFileEvent(uri, 'created');
        });

        // Handle file changes (for update detection)
        watcher.onDidChange(async (uri) => {
            console.log(`File changed: ${uri.fsPath}`);
            await this.handleFileEvent(uri, 'changed');
        });

        // Handle file deletion
        watcher.onDidDelete(async (uri) => {
            console.log(`File deleted: ${uri.fsPath}`);
            await this.handleFileEvent(uri, 'deleted');
        });

        this.watchers.push(watcher);
    }

    private async handleFileEvent(uri: vscode.Uri, eventType: 'created' | 'changed' | 'deleted'): Promise<void> {
        try {
            const filePath = uri.fsPath;

            // CRITICAL: Prevent infinite loop by ignoring files in markdown directory
            const markdownSubdirName = this.configManager.getMarkdownSubdirectoryName();
            if (filePath.includes(`/${markdownSubdirName}/`) || filePath.includes(`\\${markdownSubdirName}\\`)) {
                console.log(`Ignoring file in markdown directory: ${filePath}`);
                return;
            }

            if (eventType === 'deleted') {
                // Handle file deletion
                await this.converter.handleFileDeleted(filePath);
                return;
            }

            // Handle file creation/change
            const fileExtension = path.extname(filePath).toLowerCase();

            // Check if this extension should be processed (either for conversion or copying)
            if (!this.shouldProcessFile(fileExtension)) {
                return;
            }

            // Add a small delay to ensure file is fully written
            await new Promise(resolve => setTimeout(resolve, 1000));

            // Process the file (convert or copy)
            await this.converter.processFile(filePath);

        } catch (error) {
            console.error(`Error handling file event for ${uri.fsPath}:`, error);
            vscode.window.showErrorMessage(`Failed to process file: ${path.basename(uri.fsPath)}`);
        }
    }

    private reinitializeWatchers(): void {
        console.log('Reinitializing file watchers due to configuration change');
        this.initializeWatchers();
    }

    private disposeWatchers(): void {
        this.watchers.forEach(watcher => watcher.dispose());
        this.watchers = [];
    }

    /**
     * Check if a file should be processed (either converted or copied)
     */
    private shouldProcessFile(fileExtension: string): boolean {
        // Process files that need conversion
        const supportedExtensions = this.configManager.getSupportedExtensions();
        if (supportedExtensions.includes(fileExtension)) {
            return true;
        }

        // Also process files that should be copied to markdown directory
        const copyableExtensions = [
            '.md', '.markdown', '.mdown', '.mkd', '.mkdn',  // Markdown files
            '.txt', '.text',                                // Plain text files
            '.json', '.jsonc',                             // JSON files
            '.xml', '.html', '.htm',                       // Markup files
            '.csv', '.tsv',                                // Simple data files
            '.log',                                        // Log files
            '.yaml', '.yml',                               // YAML files
            '.toml', '.ini', '.cfg', '.conf',             // Config files
            '.sql',                                        // SQL files
        ];

        return copyableExtensions.includes(fileExtension);
    }

    dispose(): void {
        this.disposeWatchers();
    }
}
