const express = require('express');
const axios = require('axios');
const { JSDOM } = require('jsdom');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const domainRulesLink = "https://muhammadtaqi512q-oss.github.io/.mt/domains";
const websitesDataLink = "https://muhammadtaqi512q-oss.github.io/.mt/data";

// Serve static HTML/CSS files from root
app.use(express.static(path.join(__dirname, 'public')));

// Secure Backend Endpoint for Searching
app.get('/api/search', async (req, res) => {
    try {
        const query = (req.query.q || '').toLowerCase().trim();
        if (!query) return res.json([]);

        // 1. Fetch & Parse Domain Rules on Backend
        const ruleRes = await axios.get(domainRulesLink);
        const ruleDom = new JSDOM(ruleRes.data);
        const ruleText = ruleDom.window.document.getElementById('target-link').textContent.toLowerCase();

        const rankingRules = {
            p1: ruleText.match(/p1:\s*includes\s*(.*?)(?=\s*p2|$)/)?.[1].split(',').map(s => s.trim().replace('.', '')) || [],
            p2: ruleText.match(/p2:\s*includes\s*(.*?)(?=\s*p3|$)/)?.[1].split(',').map(s => s.trim().replace('.', '')) || [],
            p3: ruleText.match(/p3:\s*includes\s*(.*?)(?=\.|$)/)?.[1].split(',').map(s => s.trim().replace('.', '')) || []
        };

        // 2. Fetch & Parse Website Data on Backend
        const webRes = await axios.get(websitesDataLink);
        const webDom = new JSDOM(webRes.data);
        const webParas = webDom.window.document.querySelectorAll('p');
        
        let websiteDB = [];
        webParas.forEach(p => {
            const txt = p.textContent;
            const n = txt.match(/NAME\s+(.*?)\s+LINK/)?.[1]?.trim();
            const l = txt.match(/LINK\s+(.*?)\s+SOURCE/)?.[1]?.trim();
            const s = txt.match(/SOURCE\s+(.*)/)?.[1]?.trim();
            if(n && l && s) websiteDB.push({ name: n, display: l, source: s });
        });

        // Helper function for priority calculation
        const getPriorityScore = (url) => {
            const link = url.toLowerCase();
            const parts = link.split('.');
            const ext = parts[parts.length - 1];
            const isSub = (parts[0] !== 'www' && parts[0] !== 'mmm' && parts.length > 2);

            if (rankingRules.p1.includes(ext)) return isSub ? 1.5 : 1;
            if (rankingRules.p2.includes(ext)) return isSub ? 2.5 : 2;
            if (rankingRules.p3.includes(ext)) return isSub ? 3.5 : 3;
            return 10;
        };

        // Filter and Sort Data
        const filtered = websiteDB.filter(i => i.name.toLowerCase().includes(query) || i.display.toLowerCase().includes(query));
        filtered.sort((a, b) => getPriorityScore(a.display) - getPriorityScore(b.display));

        // Attach pre-calculated rankings to objects
        const results = filtered.map(item => ({
            ...item,
            score: Math.floor(getPriorityScore(item.display))
        }));

        res.json(results);
    } catch (error) {
        console.error("Backend Search Error:", error);
        res.status(500).json({ error: "Internal Server Engine Error" });
    }
});

app.listen(PORT, () => {
    console.log(`Nexura Core Engine Active on Port ${PORT}`);
});
