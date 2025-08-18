import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

interface LocalizedStrings {
    [key: string]: string;
}

export class I18nManager {
    private static instance: I18nManager;
    private localizedStrings: LocalizedStrings = {};
    private currentLocale: string = 'en';

    private constructor(private extensionPath: string) {
        this.loadLocalizedStrings();
    }

    public static getInstance(extensionPath?: string): I18nManager {
        if (!I18nManager.instance) {
            if (!extensionPath) {
                throw new Error('Extension path is required for first initialization');
            }
            I18nManager.instance = new I18nManager(extensionPath);
        }
        return I18nManager.instance;
    }

    private loadLocalizedStrings(): void {
        // Get VSCode's current locale
        this.currentLocale = vscode.env.language || 'en';
        
        // Try to load locale-specific strings first
        let localeFile = path.join(this.extensionPath, `package.nls.${this.currentLocale}.json`);
        
        // If locale-specific file doesn't exist, try fallback locales
        if (!fs.existsSync(localeFile)) {
            // Try language without region (e.g., 'zh' instead of 'zh-cn')
            const languageOnly = this.currentLocale.split('-')[0];
            if (languageOnly !== this.currentLocale) {
                localeFile = path.join(this.extensionPath, `package.nls.${languageOnly}.json`);
            }
            
            // If still not found, use default English
            if (!fs.existsSync(localeFile)) {
                localeFile = path.join(this.extensionPath, 'package.nls.json');
            }
        }

        try {
            if (fs.existsSync(localeFile)) {
                const content = fs.readFileSync(localeFile, 'utf8');
                this.localizedStrings = JSON.parse(content);
            }
        } catch (error) {
            console.error('Failed to load localized strings:', error);
            // Fallback to empty object, will use keys as values
            this.localizedStrings = {};
        }
    }

    public localize(key: string, ...args: any[]): string {
        let message = this.localizedStrings[key] || key;
        
        // Replace placeholders {0}, {1}, etc. with provided arguments
        if (args.length > 0) {
            message = message.replace(/\{(\d+)\}/g, (match, index) => {
                const argIndex = parseInt(index, 10);
                return argIndex < args.length ? String(args[argIndex]) : match;
            });
        }
        
        return message;
    }

    public getCurrentLocale(): string {
        return this.currentLocale;
    }

    // Convenience method for common messages
    public getMessage(key: string, ...args: any[]): string {
        return this.localize(`message.${key}`, ...args);
    }

    public getStatusText(key: string, ...args: any[]): string {
        return this.localize(`status.${key}`, ...args);
    }

    public getConfigDescription(key: string, ...args: any[]): string {
        return this.localize(`config.${key}`, ...args);
    }

    public getCommandTitle(key: string, ...args: any[]): string {
        return this.localize(`command.${key}`, ...args);
    }
}

// Convenience function for easy access
export function localize(key: string, ...args: any[]): string {
    return I18nManager.getInstance().localize(key, ...args);
}

export function getMessage(key: string, ...args: any[]): string {
    return I18nManager.getInstance().getMessage(key, ...args);
}

export function getStatusText(key: string, ...args: any[]): string {
    return I18nManager.getInstance().getStatusText(key, ...args);
}
