const fs = require('fs').promises;
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Enter the title of the paper: ", async (userInput) => {
    console.log(`Searching for paper with title: ${userInput}`);

    const metaDirectory = "./cit-HepTh-abstracts";
    const pid = await searchTitle(metaDirectory, userInput);

    if (pid === null) {
        console.log("Title didn't match. No paper found.");
    } else {
        console.log(`Paper found with PID: ${pid}`);
    }

    rl.close();
});

async function extractTitleAndGetPid(filePath, title) {
    try {
        const content = await fs.readFile(filePath, 'utf-8');
        const lines = content.split('\n');

        let inTitleSection = false;
        let extractedTitle = '';

        for (const line of lines) {
            if (line.startsWith('Title:')) {
                inTitleSection = true;
                extractedTitle = line.substring('Title:'.length).trim();
            } else if (inTitleSection && line.startsWith('Authors:')) {
                inTitleSection = false;
                break;
            } else if (inTitleSection) {
                extractedTitle += ' ' + line.trim();
            }
        }

        extractedTitle = extractedTitle.replace(/(\r\n|\n|\r)/gm, '').trim();

        if (extractedTitle.toLowerCase().includes(title.toLowerCase())) {
            const pidMatch = content.match(/hep-th\/(\d+)/);
            if (pidMatch) {
                const pid = pidMatch[1];
                return pid;
            }
        }
    } catch (error) {
        console.error(`Error reading file ${filePath}: ${error.message}`);
    }

    return null;
}

async function searchTitle(directory, title) {
    const subdirectories = await fs.readdir(directory, { withFileTypes: true });

    const results = await Promise.all(subdirectories.map(async (subdir) => {
        if (subdir.isDirectory()) {
            const subdirPath = path.join(directory, subdir.name);
            const filesInSubdir = await fs.readdir(subdirPath, { withFileTypes: true });

            for (const fileInSubdir of filesInSubdir) {
                const filePath = path.join(subdirPath, fileInSubdir.name);

                if (fileInSubdir.isFile() && fileInSubdir.name.endsWith('.abs')) {
                    const pid = await extractTitleAndGetPid(filePath, title);
                    if (pid !== null) {
                        return pid;
                    }
                }
            }
        }
        return null;
    }));

    return results.find(result => result !== null) || null;
}
