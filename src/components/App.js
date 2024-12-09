import React from 'react';
import ITAssetTable from './ITAssetTable';
import ProgressBar from './ProgressBar';

const App = () => (
  <div>
    <h1>IT Asset Scanner</h1>
    <ProgressBar />
    <ITAssetTable />
  </div>
);

export default App;
