import * as vscode from 'vscode';
import * as path from 'path';
import { MarkitdownConverter } from './converter';
import { ConfigurationManager } from './configuration';
import { StatusManager } from './statusManager';
import { ProjectManager } from './projectManager';

export class FileWatcher implements vscode.Disposable {
    private watchers: vscode.FileSystemWatcher[] = [];
    private converter: MarkitdownConverter;
    private configManager: ConfigurationManager;
    private statusManager: StatusManager;
    private projectManager: ProjectManager;

    constructor(converter: MarkitdownConverter, configManager: ConfigurationManager, statusManager: StatusManager, projectManager: ProjectManager) {
        this.converter = converter;
        this.configManager = configManager;
        this.statusManager = statusManager;
        this.projectManager = projectManager;
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

        // Auto-convert functionality has been disabled
        // Files will only be converted in two scenarios:
        // 1. When folder is opened and user confirms conversion
        // 2. Manual conversion via right-click context menu
        console.log('File watcher disabled - auto-convert functionality removed');
        return;
    }

    private async handleFileEvent(uri: vscode.Uri, eventType: 'created' | 'changed' | 'deleted'): Promise<void> {
        try {
            const filePath = uri.fsPath;
            const fileName = path.basename(filePath);

            // CRITICAL: Prevent infinite loop by ignoring files in markdown directory
            const markdownSubdirName = this.configManager.getMarkdownSubdirectoryName();
            if (filePath.includes(`/${markdownSubdirName}/`) || filePath.includes(`\\${markdownSubdirName}\\`)) {
                console.log(`Ignoring file in markdown directory: ${filePath}`);
                return;
            }

            // Ignore DocuGenius configuration files
            if (fileName === '.docugenius.json' || fileName === '.docugenius.example.json') {
                console.log(`Ignoring DocuGenius configuration file: ${filePath}`);
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
