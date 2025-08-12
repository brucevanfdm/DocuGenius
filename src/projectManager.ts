import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export interface ProjectConfig {
    enabled: boolean;
    autoConvert: boolean;
    markdownSubdirectoryName: string;
    supportedExtensions: string[];
    lastActivated?: string;
}

export class ProjectManager {
    private static readonly CONFIG_FILE_NAME = '.docugenius.json';
    private static readonly DEFAULT_CONFIG: ProjectConfig = {
        enabled: false,
        autoConvert: true,
        markdownSubdirectoryName: 'kb',
        supportedExtensions: ['.docx', '.xlsx', '.pptx', '.pdf'],
        lastActivated: new Date().toISOString()
    };

    /**
     * 检查当前工作区是否启用了 DocuGenius
     */
    isProjectEnabled(): boolean {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            return false;
        }

        const rootPath = workspaceFolders[0].uri.fsPath;
        const configPath = path.join(rootPath, ProjectManager.CONFIG_FILE_NAME);
        
        if (fs.existsSync(configPath)) {
            try {
                const config = this.loadProjectConfig(rootPath);
                return config.enabled;
            } catch (error) {
                console.error('Error reading project config:', error);
                return false;
            }
        }

        // 如果没有配置文件，检查是否已存在 kb 文件夹
        return this.hasExistingKbFolder(rootPath);
    }

    /**
     * 检查项目中是否已存在 kb 文件夹（说明之前使用过）
     */
    private hasExistingKbFolder(rootPath: string): boolean {
        const kbPath = path.join(rootPath, 'kb');
        return fs.existsSync(kbPath) && fs.statSync(kbPath).isDirectory();
    }

    /**
     * 检查项目中是否有可转换的文档文件
     */
    hasConvertibleFiles(rootPath?: string): boolean {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            return false;
        }

        const targetPath = rootPath || workspaceFolders[0].uri.fsPath;
        const supportedExtensions = ['.docx', '.xlsx', '.pptx', '.pdf'];
        
        try {
            const files = fs.readdirSync(targetPath);
            return files.some(file => {
                const ext = path.extname(file).toLowerCase();
                return supportedExtensions.includes(ext);
            });
        } catch (error) {
            console.error('Error checking for convertible files:', error);
            return false;
        }
    }

    /**
     * 为当前项目启用 DocuGenius
     */
    async enableForProject(config?: Partial<ProjectConfig>, showConvertPrompt: boolean = false): Promise<boolean> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showErrorMessage('No workspace folder is open');
            return false;
        }

        const rootPath = workspaceFolders[0].uri.fsPath;
        const projectConfig: ProjectConfig = {
            ...ProjectManager.DEFAULT_CONFIG,
            ...config,
            enabled: true,
            lastActivated: new Date().toISOString()
        };

        try {
            await this.saveProjectConfig(rootPath, projectConfig);
            
            if (showConvertPrompt && this.hasConvertibleFiles(rootPath)) {
                const choice = await vscode.window.showInformationMessage(
                    `✅ DocuGenius 已启用！检测到项目中有可转换的文档文件，是否立即转换？`,
                    '立即转换',
                    '稍后手动转换'
                );
                
                if (choice === '立即转换') {
                    // 触发文件夹转换命令
                    vscode.commands.executeCommand('documentConverter.convertFolder', vscode.Uri.file(rootPath));
                }
            } else {
                vscode.window.showInformationMessage(
                    `✅ DocuGenius 已为当前项目启用！文档将自动转换到 "${projectConfig.markdownSubdirectoryName}" 文件夹。`
                );
            }
            
            return true;
        } catch (error) {
            console.error('Error enabling project:', error);
            vscode.window.showErrorMessage('Failed to enable DocuGenius for this project');
            return false;
        }
    }

    /**
     * 为当前项目禁用 DocuGenius
     */
    async disableForProject(): Promise<boolean> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            return false;
        }

        const rootPath = workspaceFolders[0].uri.fsPath;
        const config = this.loadProjectConfig(rootPath);
        config.enabled = false;

        try {
            await this.saveProjectConfig(rootPath, config);
            vscode.window.showInformationMessage('DocuGenius 已为当前项目禁用');
            return true;
        } catch (error) {
            console.error('Error disabling project:', error);
            vscode.window.showErrorMessage('Failed to disable DocuGenius for this project');
            return false;
        }
    }

    /**
     * 加载项目配置
     */
    loadProjectConfig(rootPath?: string): ProjectConfig {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            return { ...ProjectManager.DEFAULT_CONFIG };
        }

        const targetPath = rootPath || workspaceFolders[0].uri.fsPath;
        const configPath = path.join(targetPath, ProjectManager.CONFIG_FILE_NAME);

        if (!fs.existsSync(configPath)) {
            return { ...ProjectManager.DEFAULT_CONFIG };
        }

        try {
            const configContent = fs.readFileSync(configPath, 'utf8');
            const config = JSON.parse(configContent) as ProjectConfig;
            
            // 合并默认配置以确保所有字段都存在
            return { ...ProjectManager.DEFAULT_CONFIG, ...config };
        } catch (error) {
            console.error('Error parsing project config:', error);
            return { ...ProjectManager.DEFAULT_CONFIG };
        }
    }

    /**
     * 保存项目配置
     */
    private async saveProjectConfig(rootPath: string, config: ProjectConfig): Promise<void> {
        const configPath = path.join(rootPath, ProjectManager.CONFIG_FILE_NAME);
        const configContent = JSON.stringify(config, null, 2);
        
        fs.writeFileSync(configPath, configContent, 'utf8');
    }

    /**
     * 显示项目启用确认对话框
     */
    async showEnableDialog(): Promise<boolean> {
        const choice = await vscode.window.showInformationMessage(
            '🔍 检测到此项目包含文档文件。是否要为此项目启用 DocuGenius 自动转换功能？',
            {
                modal: true,
                detail: '启用后，DocuGenius 将自动监听文档变化并转换为 Markdown 格式，存储在 "kb" 文件夹中。\n\n您可以随时在设置中禁用此功能。'
            },
            '启用',
            '不启用',
            '稍后提醒'
        );

        switch (choice) {
            case '启用':
                return await this.enableForProject(undefined, true);
            case '不启用':
                // 创建配置文件但设置为禁用，避免重复提醒
                await this.saveProjectConfig(
                    vscode.workspace.workspaceFolders![0].uri.fsPath,
                    { ...ProjectManager.DEFAULT_CONFIG, enabled: false }
                );
                return false;
            case '稍后提醒':
            default:
                return false;
        }
    }

    /**
     * 获取项目配置文件路径
     */
    getConfigFilePath(): string | null {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            return null;
        }

        return path.join(workspaceFolders[0].uri.fsPath, ProjectManager.CONFIG_FILE_NAME);
    }

    /**
     * 检查是否应该显示启用提示
     */
    shouldShowEnablePrompt(): boolean {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            return false;
        }

        const rootPath = workspaceFolders[0].uri.fsPath;
        const configPath = path.join(rootPath, ProjectManager.CONFIG_FILE_NAME);
        
        // 如果已有配置文件，不显示提示
        if (fs.existsSync(configPath)) {
            return false;
        }

        // 如果已有 kb 文件夹，自动启用，不显示提示
        if (this.hasExistingKbFolder(rootPath)) {
            this.enableForProject();
            return false;
        }

        // 如果有可转换文件，显示提示
        return this.hasConvertibleFiles(rootPath);
    }
}