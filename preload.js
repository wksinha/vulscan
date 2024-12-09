const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getSystemAssets: () => ipcRenderer.invoke('get-system-assets'),
});
