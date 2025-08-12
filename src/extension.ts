import * as vscode from 'vscode';
import { FileWatcher } from './fileWatcher';
import { MarkitdownConverter } from './converter';
import { ConfigurationManager } from './configuration';
import { StatusManager } from './statusManager';
import { ProjectManager } from './projectManager';

let fileWatcher: FileWatcher | undefined;
let statusManager: StatusManager | undefined;
let projectManager: ProjectManager | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('DocuGenius is now active!');

    // Initialize project manager
    projectManager = new ProjectManager();

    // Initialize configuration manager
    const configManager = new ConfigurationManager();
    configManager.setProjectManager(projectManager);

    // Initialize status manager
    statusManager = new StatusManager(configManager);

    // Initialize converter
    const converter = new MarkitdownConverter(context, configManager, statusManager);

    // Auto-convert functionality has been disabled
    // File watcher is no longer initialized automatically
    
    // Check if we should show enable prompt for new projects
    if (!projectManager.isProjectEnabled()) {
        setTimeout(() => {
            if (projectManager!.shouldShowEnablePrompt()) {
                projectManager!.showEnableDialog().then(enabled => {
                    if (enabled && statusManager) {
                        // Show status but don't initialize file watcher
                        statusManager.showWatcherStatus(false, configManager.getSupportedExtensions());
                    }
                });
            }
        }, 2000); // 延迟2秒，避免启动时过于突兀
    }
    
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

    // Project management commands
    const enableProjectCommand = vscode.commands.registerCommand('documentConverter.enableProject', async () => {
        if (!projectManager || !statusManager) return;
        
        const enabled = await projectManager.enableForProject(undefined, true);
        if (enabled) {
            // Auto-convert functionality has been disabled
            // Only manual conversion and folder opening conversion are supported
            statusManager.showWatcherStatus(false, configManager.getSupportedExtensions());
        }
    });

    const disableProjectCommand = vscode.commands.registerCommand('documentConverter.disableProject', async () => {
        if (!projectManager || !statusManager) return;
        
        await projectManager.disableForProject();
        if (fileWatcher) {
            fileWatcher.dispose();
            fileWatcher = undefined;
            statusManager.showWatcherStatus(false, []);
        }
    });

    const showProjectStatusCommand = vscode.commands.registerCommand('documentConverter.showProjectStatus', () => {
        if (!projectManager) return;
        
        const isEnabled = projectManager.isProjectEnabled();
        const configPath = projectManager.getConfigFilePath();
        
        vscode.window.showInformationMessage(
            `项目状态: ${isEnabled ? '已启用' : '未启用'}\n配置文件: ${configPath || '不存在'}`,
            isEnabled ? '禁用项目' : '启用项目',
            '打开配置文件'
        ).then(choice => {
            if (choice === '启用项目') {
                vscode.commands.executeCommand('documentConverter.enableProject');
            } else if (choice === '禁用项目') {
                vscode.commands.executeCommand('documentConverter.disableProject');
            } else if (choice === '打开配置文件' && configPath) {
                vscode.workspace.openTextDocument(configPath).then(doc => {
                    vscode.window.showTextDocument(doc);
                });
            }
        });
    });

    // Add disposables to context
    context.subscriptions.push(
        convertFileCommand,
        convertFolderCommand,
        enableProjectCommand,
        disableProjectCommand,
        showProjectStatusCommand,
        statusManager
    );

    // Add file watcher if it exists
    if (fileWatcher) {
        context.subscriptions.push(fileWatcher);
    }

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
