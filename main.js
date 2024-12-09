const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { exec } = require('child_process');
const { spawn } = require('child_process');


async function createWindow() {
    const isDev = (await import('electron-is-dev')).default;

    const win = new BrowserWindow({
        width: 1024,
        height: 768,
        webPreferences: {
            preload: `${__dirname}/preload.js`,
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    const startUrl = isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, '../build/index.html')}`;
    win.loadURL(startUrl);
}

app.whenReady().then(() => {
    ipcMain.handle('get-it-info', (event) => {
        const pythonProcess = spawn('python3', [path.join(__dirname, 'asset_scanner.py')]);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`Output: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            console.log(`Python script finished with exit code ${code}`);
        });
    });

    createWindow();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
