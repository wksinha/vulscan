const express = require('express');
const app = express();
const PORT = 5000;

let isScanning = false;
let progress = 0;
let vulnerabilities = [];

app.get('/api/scan/start', (req, res) => {
    isScanning = true;
    progress = 0;
    vulnerabilities = [];
    res.json({ message: 'Scan started' });
});

app.get('/api/scan/stop', (req, res) => {
    isScanning = false;
    progress = 0;
    res.json({ message: 'Scan stopped' });
});

app.get('/api/scan/progress', (req, res) => {
    if (isScanning) {
        progress = Math.min(progress + 10, 100);
        if (progress === 100) isScanning = false;
    }
    res.json({ progress, vulnerabilities });
});

app.post('/api/patch/:id', (req, res) => {
    const id = req.params.id;
    res.json({ message: `Patch initiated for vulnerability ${id}` });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
