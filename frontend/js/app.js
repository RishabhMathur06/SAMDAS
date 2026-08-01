// The URL of our FastAPI backend
const API_URL = "http://127.0.0.1:8000/api/v1/ledger/sessions";

async function fetchLedgerData() {
    try {
        // 1. Send a GET request to the API
        const response = await fetch(API_URL);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        // 2. Convert the response to JSON
        const sessions = await response.json();
        
        // 3. Render the data into the HTML table
        renderTable(sessions);

    } catch (error) {
        console.error("Failed to fetch ledger data:", error);
        document.getElementById("ledger-body").innerHTML = `
            <tr>
                <td colspan="4" style="text-align:center; color: red;">
                    Failed to connect to Firewall API. Is Uvicorn running?
                </td>
            </tr>
        `;
    }
}

function renderTable(sessions) {
    const tableBody = document.getElementById("ledger-body");
    tableBody.innerHTML = ""; // Clear existing rows

    if (sessions.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="4" style="text-align:center;">No cryptographic sessions logged yet.</td></tr>`;
        return;
    }

    // Loop through every session and create an HTML row for it
    sessions.forEach(session => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>#${session.id}</td>
            <td>${session.timestamp}</td>
            <td class="hash-cell">${session.root_hash}</td>
            <td><span class="status-badge">VERIFIED</span></td>
        `;

        tableBody.appendChild(row);
    });
}

// Automatically fetch the data when the page loads
document.addEventListener("DOMContentLoaded", fetchLedgerData);
