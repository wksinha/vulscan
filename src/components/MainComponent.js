import React, { useState } from 'react';
import './Vulnerabilities.css';

const MainComponent = () => {
    const [activeTab, setActiveTab] = useState('vulnerabilities');

    const renderTabContent = () => {
        switch (activeTab) {
            case 'vulnerabilities':
                return (
                    <div>
                        <h2>Vulnerabilities</h2>
                        <p>vulnerability data</p>
                    </div>
                );
            case 'patches':
                return (
                    <div>
                        <h2>Patches</h2>
                        <p>patching</p>
                    </div>
                );
            case 'settings':
                return (
                    <div>
                        <h2>Settings</h2>
                        <p>settings</p>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="container">
            {/* Sidebar */}
            <div className="sidebar">
                <h3>Vulnerability Scanner</h3>
                <ul className="nav flex-column">
                    <li className="nav-item">
                        <button
                            className={`nav-link ${activeTab === 'vulnerabilities' ? 'active' : ''}`}
                            onClick={() => setActiveTab('vulnerabilities')}
                        >
                            Vulnerabilities
                        </button>
                    </li>
                    <li className="nav-item">
                        <button
                            className={`nav-link ${activeTab === 'patches' ? 'active' : ''}`}
                            onClick={() => setActiveTab('patches')}
                        >
                            Patches
                        </button>
                    </li>
                    <li className="nav-item">
                        <button
                            className={`nav-link ${activeTab === 'settings' ? 'active' : ''}`}
                            onClick={() => setActiveTab('settings')}
                        >
                            Settings
                        </button>
                    </li>
                </ul>
            </div>

            <div className="main-content">
                {renderTabContent()}
            </div>
        </div>
    );
};

export default MainComponent;
