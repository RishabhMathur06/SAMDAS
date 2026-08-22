// The URL of our FastAPI backend
const API_URL = "http://127.0.0.1:8000/api/v1/ledger/sessions";
// URL of websockets
const WS_URL = "ws://127.0.0.1:8000/ws/dashboard";

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

    // Load historical sessions.
    sessions.forEach(session => {
        // Assume VERIFIED for old history unless specified otherwise.
        addSessionToTable(session.id, session.timestamp, session.root_hash, session.verdict || "Verified");
    });
}

// Helper to inject a single row at the TOP of the table.
function addSessionToTable(id, timestamp, hash, verdict) {
    const tableBody = document.getElementById("ledger-body");
    const row = document.createElement("tr")

    // Dynamic styling based on the ML Auditor's verdict.
    let badgeClass = "status-badge";
    if (verdict === "REJECTED") badgeClass += " status-rejected";
    else if (verdict === "APPROVED") badgeClass += " status-approved";

    row.innerHTML = `
        <td>#${id}</td>
        <td>${timestamp}</td>
        <td class="hash-cell">${hash}</td>
        <td><span class="${badgeClass}">${verdict}</span></td>
    `;

    // Inject at the very top of the table.
    tableBody.insertBefore(row, tableBody.firstChild);
}

// 2. LIVE WEBSOCKET CONNECTION
function connectWebSocket() {
    console.log("Attempting to connect to SAMDAS Control Plane...");
    const socket = new WebSocket(WS_URL);

    socket.onopen = function(e) {
        console.log("[WebSocket] Connection established. Listening for live sessions...");
    };

    socket.onmessage = function(event) {
        // Triggered instantly when FastAPI broacasts a new AI thought.
        const liveSession = JSON.parse(event.data);
        console.log("[LIVE EVENT INCOMING]:",liveSession);

        // Add it to the top of the table instantly.
        addSessionToTable(
            liveSession.id,
            liveSession.timestamp,
            liveSession.root_hash,
            liveSession.verdict
        );
    };

    socket.onclose = function(event) {
        console.log("[WebSocket] Connection died. reconnecting in 3 seconds...")
        setTimeout(connectWebSocket, 3000);
    };
}

// Start everything when page loads.
document.addEventListener("DOMContentLoaded", () => {
    fetchLedgerData();
    connectWebSocket();
});