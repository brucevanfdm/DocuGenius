import * as vscode from 'vscode';
import { FileWatcher } from './fileWatcher';
import { MarkitdownConverter } from './converter';
import { ConfigurationManager } from './configuration';
import { StatusManager } from './statusManager';

let fileWatcher: FileWatcher | undefined;
let statusManager: StatusManager | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('DocuGenius is now active!');

    // Initialize configuration manager
    const configManager = new ConfigurationManager();

    // Initialize status manager
    statusManager = new StatusManager(configManager);

    // Initialize converter
    const converter = new MarkitdownConverter(context, configManager, statusManager);

    // Initialize file watcher
    fileWatcher = new FileWatcher(converter, configManager, statusManager);
    
    // Register commands
    const convertFileCommand = vscode.commands.registerCommand('documentConverter.convertFile', async (uri: vscode.Uri) => {
        if (uri && uri.fsPath) {
            // Force conversion for manual command to ensure fresh conversion
            await converter.processFile(uri.fsPath, true);
        } else {
            // If no URI provided, ask user to select a file
            const fileUri = await vscode.window.showOpenDialog({
                canSelectFiles: true,
                canSelectFolders: false,
                canSelectMany: false,
                filters: {
                    'All Supported Files': ['docx', 'xlsx', 'pptx', 'pdf', 'txt', 'md', 'json', 'xml', 'html', 'csv', 'yaml', 'sql']
                }
            });

            if (fileUri && fileUri[0]) {
                // Force conversion for manual selection
                await converter.processFile(fileUri[0].fsPath, true);
            }
        }
    });


    const convertFolderCommand = vscode.commands.registerCommand('documentConverter.convertFolder', async (uri: vscode.Uri) => {
        if (uri && uri.fsPath) {
            await converter.convertFolder(uri.fsPath);
        } else {
            // If no URI provided, ask user to select a folder
            const folderUri = await vscode.window.showOpenDialog({
                canSelectFiles: false,
                canSelectFolders: true,
                canSelectMany: false
            });

            if (folderUri && folderUri[0]) {
                await converter.convertFolder(folderUri[0].fsPath);
            }
        }
    });

    // Add disposables to context
    context.subscriptions.push(
        convertFileCommand,
        convertFolderCommand,
        fileWatcher,
        statusManager
    );

    // Show activation message and update status
    statusManager.updateStatusBar('Ready');
    statusManager.showWatcherStatus(configManager.isAutoConvertEnabled(), configManager.getSupportedExtensions());
    vscode.window.showInformationMessage('DocuGenius is ready!');
}

export function deactivate() {
    if (fileWatcher) {
        fileWatcher.dispose();
    }
    if (statusManager) {
        statusManager.dispose();
    }
}
