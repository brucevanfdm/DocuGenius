const fs = require('fs');
const path = require('path');

// Test i18n files
function testI18nFiles() {
    console.log('Testing i18n files...\n');
    
    const files = [
        'package.nls.json',
        'package.nls.zh-cn.json'
    ];
    
    let allKeys = new Set();
    let results = {};
    
    // Load all files and collect keys
    for (const file of files) {
        try {
            const content = fs.readFileSync(file, 'utf8');
            const data = JSON.parse(content);
            results[file] = data;
            
            Object.keys(data).forEach(key => allKeys.add(key));
            console.log(`✓ Loaded ${file}: ${Object.keys(data).length} keys`);
        } catch (error) {
            console.error(`✗ Failed to load ${file}:`, error.message);
        }
    }
    
    console.log(`\nTotal unique keys: ${allKeys.size}\n`);
    
    // Check for missing keys
    for (const file of files) {
        if (results[file]) {
            const fileKeys = new Set(Object.keys(results[file]));
            const missingKeys = [...allKeys].filter(key => !fileKeys.has(key));
            
            if (missingKeys.length > 0) {
                console.log(`⚠ Missing keys in ${file}:`);
                missingKeys.forEach(key => console.log(`  - ${key}`));
                console.log();
            } else {
                console.log(`✓ ${file} has all keys`);
            }
        }
    }
    
    // Test some key translations
    console.log('\nSample translations:');
    const sampleKeys = [
        'extension.displayName',
        'extension.description',
        'command.convertFile.title',
        'message.ready',
        'status.ready'
    ];
    
    for (const key of sampleKeys) {
        console.log(`\n${key}:`);
        for (const file of files) {
            if (results[file] && results[file][key]) {
                const lang = file === 'package.nls.json' ? 'en' : 'zh-cn';
                console.log(`  ${lang}: ${results[file][key]}`);
            }
        }
    }
}

// Test package.json placeholders
function testPackageJsonPlaceholders() {
    console.log('\n\nTesting package.json placeholders...\n');
    
    try {
        const packageContent = fs.readFileSync('package.json', 'utf8');
        const packageData = JSON.parse(packageContent);
        
        // Check if placeholders are used
        const placeholderPattern = /%[^%]+%/g;
        const jsonString = JSON.stringify(packageData, null, 2);
        const placeholders = jsonString.match(placeholderPattern) || [];
        
        console.log(`Found ${placeholders.length} placeholders in package.json:`);
        const uniquePlaceholders = [...new Set(placeholders)];
        uniquePlaceholders.forEach(placeholder => {
            console.log(`  ${placeholder}`);
        });
        
        // Check if all placeholders have corresponding keys in nls files
        const nlsContent = fs.readFileSync('package.nls.json', 'utf8');
        const nlsData = JSON.parse(nlsContent);
        
        console.log('\nPlaceholder validation:');
        for (const placeholder of uniquePlaceholders) {
            const key = placeholder.slice(1, -1); // Remove % symbols
            if (nlsData[key]) {
                console.log(`  ✓ ${placeholder} -> ${nlsData[key]}`);
            } else {
                console.log(`  ✗ ${placeholder} -> KEY NOT FOUND`);
            }
        }
        
    } catch (error) {
        console.error('Failed to test package.json:', error.message);
    }
}

// Run tests
testI18nFiles();
testPackageJsonPlaceholders();

console.log('\n\nI18n test completed!');
console.log('\nTo test the extension:');
console.log('1. Press F5 to launch Extension Development Host');
console.log('2. Change VSCode language: Ctrl+Shift+P -> "Configure Display Language"');
console.log('3. Restart VSCode and check if the extension UI shows in the selected language');
