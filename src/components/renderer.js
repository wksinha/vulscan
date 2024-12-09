document.getElementById('fetch-assets').addEventListener('click', async () => {
    const assetData = await window.electronAPI.getSystemAssets();
    
    const assetInfoDiv = document.getElementById('asset-info');
    assetInfoDiv.innerHTML = `
      <h3>CPU Information</h3><pre>${assetData.cpuInfo}</pre>
      <h3>Memory Information</h3><pre>${assetData.memoryInfo}</pre>
      <h3>Storage Information</h3><pre>${assetData.storageInfo}</pre>
      <h3>OS Information</h3><pre>${assetData.osInfo}</pre>
      <h3>Installed Packages</h3><pre>${assetData.installedPackages}</pre>
      <h3>Network Interfaces</h3><pre>${assetData.networkInterfaces}</pre>
    `;
  });
  