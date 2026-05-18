const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { JSDOM } = require('jsdom');

// Database URLs
const domainRulesLink = "https://muhammadtaqi512q-oss.github.io/.mt/domains";
const websitesDataLink = "https://muhammadtaqi512q-oss.github.io/.mt/data";
const templatePath = path.join(__dirname, 'template.html');

async function compileEngine() {
    try {
        console.log("JAVIS-AI-2 Core: Accessing data streaming layers...");
        
        // 1. Fetch Domain Priorities
        const ruleRes = await axios.get(domainRulesLink);
        const ruleDom = new JSDOM(ruleRes.data);
        const ruleText = ruleDom.window.document.getElementById('target-link').textContent.toLowerCase();

        const p1 = ruleText.match(/p1:\s*includes\s*(.*?)(?=\s*p2|$)/)?.[1].split(',').map(s => s.trim().replace('.', '')) || [];
        const p2 = ruleText.match(/p2:\s*includes\s*(.*?)(?=\s*p3|$)/)?.[1].split(',').map(s => s.trim().replace('.', '')) || [];
        const p3 = ruleText.match(/p3:\s*includes\s*(.*?)(?=\.|$)/)?.[1].split(',').map(s => s.trim().replace('.', '')) || [];

        // 2. Fetch Website Registry
        const webRes = await axios.get(websitesDataLink);
        const webDom = new JSDOM(webRes.data);
        const webParas = webDom.window.document.querySelectorAll('p');
        
        let websiteDB = [];
        
        const getPriorityScore = (url) => {
            const link = url.toLowerCase();
            const parts = link.split('.');
            const ext = parts[parts.length - 1];
            const isSub = (parts[0] !== 'www' && parts[0] !== 'mmm' && parts.length > 2);

            if (p1.includes(ext)) return isSub ? 1.5 : 1;
            if (p2.includes(ext)) return isSub ? 2.5 : 2;
            if (p3.includes(ext)) return isSub ? 3.5 : 3;
            return 10;
        };

        webParas.forEach(p => {
            const txt = p.textContent;
            const n = txt.match(/NAME\s+(.*?)\s+LINK/)?.[1]?.trim();
            const l = txt.match(/LINK\s+(.*?)\s+SOURCE/)?.[1]?.trim();
            const s = txt.match(/SOURCE\s+(.*)/)?.[1]?.trim();
            
            if(n && l && s) {
                const score = getPriorityScore(l);
                // Secure encryption processing (Base64)
                websiteDB.push({
                    n: Buffer.from(n).toString('base64'),
                    d: Buffer.from(l).toString('base64'),
                    s: Buffer.from(s).toString('base64'),
                    p: Math.floor(score)
                });
            }
        });

        // 3. Generate Build
        if (!fs.existsSync('./dist')) fs.mkdirSync('./dist');

        let htmlLayout = fs.readFileSync(templatePath, 'utf8');
        const secureInjection = `const _nxDB = ${JSON.stringify(websiteDB)};`;
        
        htmlLayout = htmlLayout.replace('/*INJECT_DATABASE*/', secureInjection);

        fs.writeFileSync('./dist/index.html', htmlLayout);
        console.log("JAVIS-AI-2 Master Core build sequence completed.");

    } catch (error) {
        console.error("Compilation sequence halted:", error);
        process.exit(1);
    }
}

compileEngine();
