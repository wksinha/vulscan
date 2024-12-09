// src/components/VulnerabilitiesTab.js
export default function VulnerabilitiesTab(data) {
    const tableRows = data.map((vulnerability) => `
        <tr>
            <td>${vulnerability.id}</td>
            <td>${vulnerability.component}</td>
            <td>${vulnerability.severity}</td>
            <td>${vulnerability.description}</td>
            <td>${vulnerability.patchAvailable ? 'Yes' : 'No'}</td>
        </tr>
    `).join('');

    return `
        <h2>Detected Vulnerabilities</h2>
        <table class="table table-striped table-hover">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Component</th>
                    <th>Severity</th>
                    <th>Description</th>
                    <th>Patch Available</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>
    `;
}
