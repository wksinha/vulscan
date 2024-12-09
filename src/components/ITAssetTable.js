import React, { useState, useEffect } from 'react';
import { getITAssets } from '../database/db';

const ITAssetTable = () => {
  const [assets, setAssets] = useState([]);

  useEffect(() => {
    const fetchAssets = async () => {
      const data = await getITAssets();
      setAssets(data);
    };

    fetchAssets();
  }, []);

  return (
    <div>
      <h2>IT Asset Information</h2>
      <table className="table">
        <thead>
          <tr>
            <th>OS</th>
            <th>CPU</th>
            <th>Memory (GB)</th>
            <th>Disk (GB)</th>
            <th>Network Interfaces</th>
          </tr>
        </thead>
        <tbody>
          {assets.map((asset, index) => (
            <tr key={index}>
              <td>{asset.os} {asset.os_version}</td>
              <td>{asset.cpu}</td>
              <td>{(asset.memory / 1e9).toFixed(2)}</td>
              <td>{(asset.disk / 1e9).toFixed(2)}</td>
              <td>{asset.network.join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ITAssetTable;
