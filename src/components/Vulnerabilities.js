// src/components/Vulnerabilities.js
import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Vulnerabilities.css';

function Vulnerabilities() {
    const [vulnerabilities, setVulnerabilities] = useState([]);
    const [isScanning, setIsScanning] = useState(false);
    const [scanBtnDisabled, setScanBtnDisabled] = useState(false);
    const [patchBtnDisabled, setPatchBtnDisabled] = useState(false);

    useEffect(() => {
        console.log("UE");
        console.log(isScanning);
        if (isScanning) {
            setScanBtnDisabled(true);
        } else {
            setScanBtnDisabled(false);
        }
    }, [isScanning]);

    const handleClick = () => {
        setIsScanning(true);
        fetch('http://127.0.0.1:5000/start')
            .then((response) => {
                if (!response.ok) {
                    setTimeout(() => setIsScanning(false), 1000);
                    throw new Error('Network response was not ok');
                }
                var resjson = response.json();
                console.log(resjson);
                return resjson;
            })
            .then((data) => {
                setVulnerabilities(data);
                setIsScanning(false);
            })
            .catch((error) => {
                setIsScanning(false);
                alert("Failed to Complete Scan");
                console.error('Error fetching vulnerabilities:', error);
            });
    }

    const handlePatch = (id) => {
        const confirmation = window.confirm("Are you sure you want to patch this vulnerability?");
        if (confirmation) {
            setPatchBtnDisabled(true);
            alert(`Patching vulnerability ID: ${id}`);
            const url = `http://127.0.0.1:8000/process_cvid?cvid=${encodeURIComponent(id)}`;
            fetch(url)
            .then((response) => {
                if (!response.ok) {
                    setPatchBtnDisabled(false);
                    alert("Failed to apply patch.");
                    throw new Error('Network response was not ok');
                }
                var resjson = response.json();
                console.log(resjson);
                setPatchBtnDisabled(false);
                return resjson;
            })
            .catch((error) => console.error(error));
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="text-center text-info mb-4">Vulnerability Scanner</h2>
            
            <div className="d-flex justify-content-center mb-3">
                <button 
                    className={`btn ${isScanning ? 'btn-danger' : 'btn-primary'} btn-lg`} 
                    onClick={handleClick}
                    disabled={scanBtnDisabled}
                >
                    {isScanning ? 'Scanning' : 'Start Scan'}
                </button>
            </div>

            <table className="table table-striped table-hover table-bordered shadow-sm">
                <thead className="thead-light">
                    <tr>
                        <th>ID</th>
                        <th>Component</th>
                        <th>Severity</th>
                        <th>CVSS Score</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {vulnerabilities.map((vuln) => (
                        <tr key={vuln[0]} className="table-row">
                            <td>{vuln[0]}</td>
                            <td>{"firefox"}</td>
                            <td className={`text-${
                                vuln[3] === 'CRITICAL' ? 'danger' :
                                vuln[3] === 'HIGH' ? 'warning' :
                                vuln[3] === 'MEDIUM' ? 'info' : 'secondary'
                            }`}>
                                {vuln[3]}
                            </td>
                            <td>{vuln[2]}</td>
                            <td>{vuln[4]}</td>
                            <td>
                                <button 
                                    className="btn btn-sm btn-success" 
                                    disabled={patchBtnDisabled}
                                    onClick={() => handlePatch(vuln[0])}
                                >
                                {patchBtnDisabled ? 'Patching' : 'Patch'}                                    
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Vulnerabilities;
