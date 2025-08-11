import * as vscode from 'vscode';

export class ConfigurationManager {
    private static readonly SECTION = 'documentConverter';

    /**
     * Check if auto-conversion is enabled
     */
    isAutoConvertEnabled(): boolean {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        return config.get<boolean>('autoConvert', true);
    }

    /**
     * Check if existing files should be overwritten
     */
    shouldOverwriteExisting(): boolean {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        return config.get<boolean>('overwriteExisting', true);
    }

    /**
     * Check if images should be extracted
     */
    shouldExtractImages(): boolean {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        return config.get<boolean>('extractImages', true);
    }

    /**
     * Get supported file extensions
     */
    getSupportedExtensions(): string[] {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        return config.get<string[]>('supportedExtensions', ['.docx', '.xlsx', '.pptx', '.pdf']);
    }

    /**
     * Check if files should be organized in markdown subdirectory
     */
    shouldOrganizeInSubdirectory(): boolean {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        return config.get<boolean>('organizeInSubdirectory', true);
    }

    /**
     * Get the name of the subdirectory for converted files
     */
    getMarkdownSubdirectoryName(): string {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        return config.get<string>('markdownSubdirectoryName', 'kb');
    }

    /**
     * Update a configuration value
     */
    async updateConfiguration(key: string, value: any, target?: vscode.ConfigurationTarget): Promise<void> {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        await config.update(key, value, target || vscode.ConfigurationTarget.Global);
    }

    /**
     * Get all configuration as an object
     */
    getAllConfiguration(): {
        autoConvert: boolean;
        overwriteExisting: boolean;
        extractImages: boolean;
        supportedExtensions: string[];
    } {
        return {
            autoConvert: this.isAutoConvertEnabled(),
            overwriteExisting: this.shouldOverwriteExisting(),
            extractImages: this.shouldExtractImages(),
            supportedExtensions: this.getSupportedExtensions()
        };
    }

    /**
     * Reset configuration to defaults
     */
    async resetToDefaults(): Promise<void> {
        const config = vscode.workspace.getConfiguration(ConfigurationManager.SECTION);
        await config.update('autoConvert', undefined, vscode.ConfigurationTarget.Global);
        await config.update('overwriteExisting', undefined, vscode.ConfigurationTarget.Global);
        await config.update('extractImages', undefined, vscode.ConfigurationTarget.Global);
        await config.update('supportedExtensions', undefined, vscode.ConfigurationTarget.Global);
    }

    /**
     * Validate configuration
     */
    validateConfiguration(): { isValid: boolean; errors: string[] } {
        const errors: string[] = [];
        const extensions = this.getSupportedExtensions();

        // Check if extensions array is valid
        if (!Array.isArray(extensions) || extensions.length === 0) {
            errors.push('Supported extensions must be a non-empty array');
        }

        // Check if extensions have proper format
        for (const ext of extensions) {
            if (typeof ext !== 'string' || !ext.startsWith('.')) {
                errors.push(`Invalid extension format: ${ext}. Extensions must start with a dot.`);
            }
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }
}
