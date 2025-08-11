import * as vscode from 'vscode';

export class StatusManager {
    private statusBarItem: vscode.StatusBarItem;
    private outputChannel: vscode.OutputChannel;

    constructor() {
        // Create status bar item
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
        this.statusBarItem.command = 'documentConverter.showOutput';
        
        // Create output channel
        this.outputChannel = vscode.window.createOutputChannel('DocuGenius');
        
        // Register command to show output
        vscode.commands.registerCommand('documentConverter.showOutput', () => {
            this.outputChannel.show();
        });
        
        this.updateStatusBar('Ready');
    }

    /**
     * Update status bar with current status
     */
    updateStatusBar(status: string, tooltip?: string): void {
        this.statusBarItem.text = `$(markdown) ${status}`;
        this.statusBarItem.tooltip = tooltip || `DocuGenius: ${status}`;
        this.statusBarItem.show();
    }

    /**
     * Show conversion in progress
     */
    showConversionInProgress(fileName: string): void {
        this.updateStatusBar(
            `Converting ${fileName}...`,
            `Converting ${fileName} to Markdown`
        );
        this.log(`Starting conversion: ${fileName}`);
    }

    /**
     * Show conversion success
     */
    showConversionSuccess(inputFile: string, outputFile: string): void {
        const inputName = this.getFileName(inputFile);
        const outputName = this.getFileName(outputFile);
        const outputDir = this.getDirectoryName(outputFile);

        this.updateStatusBar('Ready');
        this.log(`✓ Successfully converted: ${inputName} → ${outputDir}/${outputName}`);

        // Show temporary success message in status bar
        this.updateStatusBar(`✓ Converted ${inputName}`, `Successfully converted ${inputName} to ${outputDir}/${outputName}`);

        // Reset status bar after 3 seconds
        setTimeout(() => {
            this.updateStatusBar('Ready');
        }, 3000);
    }

    /**
     * Show conversion error
     */
    showConversionError(fileName: string, error: string): void {
        const name = this.getFileName(fileName);
        
        this.updateStatusBar('Ready');
        this.log(`✗ Failed to convert: ${name} - ${error}`, true);
        
        // Show temporary error message in status bar
        this.updateStatusBar(`✗ Failed: ${name}`, `Failed to convert ${name}: ${error}`);
        
        // Reset status bar after 5 seconds
        setTimeout(() => {
            this.updateStatusBar('Ready');
        }, 5000);
    }

    /**
     * Show batch conversion progress
     */
    showBatchProgress(current: number, total: number, currentFile?: string): void {
        const progress = `${current}/${total}`;
        const status = currentFile 
            ? `Converting ${progress}: ${this.getFileName(currentFile)}...`
            : `Converting ${progress}...`;
            
        this.updateStatusBar(status, `Batch conversion progress: ${progress}`);
        
        if (currentFile) {
            this.log(`Converting (${progress}): ${this.getFileName(currentFile)}`);
        }
    }

    /**
     * Show batch conversion complete
     */
    showBatchComplete(successCount: number, totalCount: number): void {
        const failureCount = totalCount - successCount;
        
        if (failureCount === 0) {
            this.log(`✓ Batch conversion complete: ${successCount} files converted successfully`);
            this.updateStatusBar(`✓ Converted ${successCount} files`, `Successfully converted ${successCount} files`);
        } else {
            this.log(`⚠ Batch conversion complete: ${successCount} succeeded, ${failureCount} failed`);
            this.updateStatusBar(
                `⚠ ${successCount}/${totalCount} converted`, 
                `Batch conversion: ${successCount} succeeded, ${failureCount} failed`
            );
        }
        
        // Reset status bar after 5 seconds
        setTimeout(() => {
            this.updateStatusBar('Ready');
        }, 5000);
    }

    /**
     * Show configuration change
     */
    showConfigurationChange(setting: string, value: any): void {
        this.log(`Configuration changed: ${setting} = ${value}`);
        this.updateStatusBar('Config updated', `Configuration updated: ${setting}`);
        
        // Reset status bar after 2 seconds
        setTimeout(() => {
            this.updateStatusBar('Ready');
        }, 2000);
    }

    /**
     * Show file watcher status
     */
    showWatcherStatus(enabled: boolean, extensions: string[]): void {
        if (enabled) {
            this.log(`File watcher enabled for extensions: ${extensions.join(', ')}`);
            this.updateStatusBar('Watching', `Auto-conversion enabled for: ${extensions.join(', ')}`);
        } else {
            this.log('File watcher disabled');
            this.updateStatusBar('Not watching', 'Auto-conversion is disabled');
        }

        // Reset status bar after 3 seconds
        setTimeout(() => {
            this.updateStatusBar('Ready');
        }, 3000);
    }

    /**
     * Show file skipped message
     */
    showFileSkipped(fileName: string, reason: string): void {
        this.log(`⏭ Skipped ${fileName}: ${reason}`);

        // Show temporary skip message in status bar
        this.updateStatusBar(`⏭ Skipped ${fileName}`, `Skipped ${fileName}: ${reason}`);

        // Reset status bar after 2 seconds
        setTimeout(() => {
            this.updateStatusBar('Ready');
        }, 2000);
    }

    /**
     * Log message to output channel
     */
    log(message: string, isError: boolean = false): void {
        const timestamp = new Date().toLocaleTimeString();
        const prefix = isError ? '[ERROR]' : '[INFO]';
        this.outputChannel.appendLine(`${timestamp} ${prefix} ${message}`);
    }

    /**
     * Get file name from path
     */
    private getFileName(filePath: string): string {
        return filePath.split(/[/\\]/).pop() || filePath;
    }

    /**
     * Get directory name from path
     */
    private getDirectoryName(filePath: string): string {
        const parts = filePath.split(/[/\\]/);
        return parts[parts.length - 2] || '';
    }

    /**
     * Dispose resources
     */
    dispose(): void {
        this.statusBarItem.dispose();
        this.outputChannel.dispose();
    }
}
