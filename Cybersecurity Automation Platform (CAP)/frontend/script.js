const API_URL = 'http://localhost:5000/api';

// --- Initialization & UI Logic ---
document.addEventListener('DOMContentLoaded', () => {
    // Navigation Tabs
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const pageTitleElement = document.getElementById('page-title');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active classes
            navItems.forEach(nav => nav.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active-tab'));
            
            // Add active to clicked
            item.classList.add('active');
            
            // Show corresponding tab
            const tabId = item.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active-tab');
            
            // Update Header Title
            pageTitleElement.innerText = item.querySelector('span').innerText;
            
            if(tabId === 'dashboard') {
                fetchData();
            } else if (tabId === 'scanner') {
                fetchScans();
            }
        });
    });

    // Initial Data Fetch
    fetchData();
});

// --- API Fetching Methods ---

async function fetchAlerts() {
    try {
        const response = await fetch(`${API_URL}/alerts/`);
        const data = await response.json();
        
        const tbody = document.getElementById('alerts-body');
        const alertBadge = document.getElementById('alert-badge');
        const activeCount = document.getElementById('active-alerts-count');
        
        if(data.alerts && data.alerts.length > 0) {
            tbody.innerHTML = '';
            let newAlertsCount = 0;
            
            // Sort to show newest first
            data.alerts.reverse().forEach(alert => {
                if(alert.status !== 'resolved') newAlertsCount++;
                
                const tr = document.createElement('tr');
                const date = new Date(alert.timestamp * 1000).toLocaleString();
                
                let sevClass = '';
                if(alert.severity === 'High') sevClass = 'status-high';
                else if(alert.severity === 'Medium') sevClass = 'status-medium';
                else sevClass = 'status-low';
                
                if(alert.status === 'resolved') sevClass = 'status-resolved';
                
                tr.innerHTML = `
                    <td>...${String(alert._id || alert.alert_id).slice(-6)}</td>
                    <td>${alert.type}</td>
                    <td><span class="status-badge ${sevClass}">${alert.status === 'resolved' ? 'Resolved' : alert.severity}</span></td>
                    <td>${alert.description}</td>
                    <td>${date}</td>
                    <td>
                        ${alert.status !== 'resolved' ? 
                            `<button class="btn-resolve" onclick="resolveAlert('${alert._id || alert.alert_id}')">Resolve</button>` 
                            : '<i class="fa-solid fa-check text-muted" style="color:var(--success-color)"></i>'}
                    </td>
                `;
                tbody.appendChild(tr);
            });
            
            alertBadge.innerText = `${newAlertsCount} New`;
            activeCount.innerText = newAlertsCount;
            
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No alerts found. System is secure.</td></tr>';
            alertBadge.innerText = `0 New`;
            activeCount.innerText = `0`;
        }
    } catch (e) {
        console.error("Error fetching alerts:", e);
    }
}

async function fetchScans() {
    try {
        const response = await fetch(`${API_URL}/scans/`);
        const data = await response.json();
        
        const tbody = document.getElementById('scans-body');
        const countCounter = document.getElementById('recent-scans-count');
        
        if(data.scans && data.scans.length > 0) {
            tbody.innerHTML = '';
            countCounter.innerText = data.scans.length;
            
            data.scans.slice(0, 10).forEach(scan => {
                const tr = document.createElement('tr');
                const date = new Date(scan.timestamp * 1000).toLocaleString();
                
                tr.innerHTML = `
                    <td><strong>${scan.target}</strong></td>
                    <td><span class="status-badge status-low">${scan.status}</span></td>
                    <td>${date}</td>
                    <td>${scan.open_ports ? scan.open_ports.join(', ') : 'None'}</td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (e) {
        console.error("Error fetching scans:", e);
    }
}

function fetchData() {
    fetchAlerts();
    fetchScans();
}

// --- Action Methods ---

async function resolveAlert(id) {
    if(!id) return;
    try {
        const res = await fetch(`${API_URL}/alerts/resolve/${id}`, { method: 'POST' });
        if(res.ok) {
            fetchAlerts(); // refresh
        } else {
            alert('Failed to resolve alert');
        }
    } catch(e) {
        console.error(e);
    }
}

async function runScan() {
    const input = document.getElementById('scan-target');
    const target = input.value.trim();
    if(!target) return alert('Please enter a target IP or domain');
    
    const btn = document.getElementById('run-scan-btn');
    const ogText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Scanning...';
    btn.disabled = true;
    
    document.getElementById('scan-results-container').style.display = 'block';
    const outputText = document.getElementById('scan-output-text');
    outputText.innerText = `Initializing scan on target: ${target}...\nSending packets...\n`;
    
    try {
        const response = await fetch(`${API_URL}/scans/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target })
        });
        
        const data = await response.json();
        if(response.ok) {
            outputText.innerText += `\n>> Scan Completed Successfully <<\n\n`;
            outputText.innerText += JSON.stringify(data.results, null, 2);
            fetchScans(); // refresh table
            fetchAlerts(); // a scan might generate alerts
        } else {
            outputText.innerText += `\nError: ${data.error || 'Server error'}`;
        }
    } catch(e) {
        outputText.innerText += `\nConnection Error: ${e.message}`;
    } finally {
        btn.innerHTML = ogText;
        btn.disabled = false;
        input.value = '';
    }
}

async function analyzeUrl() {
    const input = document.getElementById('ai-url-target');
    const url = input.value.trim();
    if(!url) return alert('Please enter a URL to analyze');
    
    const btn = document.getElementById('run-ai-btn');
    const ogText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
    btn.disabled = true;
    
    const resultContainer = document.getElementById('ai-results-container');
    resultContainer.classList.add('hidden');
    
    try {
        const response = await fetch(`${API_URL}/ai/analyze-url`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        if(response.ok && data.prediction) {
            const p = data.prediction;
            document.getElementById('ai-target-disp').innerText = p.url;
            document.getElementById('ai-risk-score').innerText = (p.risk_score * 100).toFixed(1);
            document.getElementById('ai-model-version').innerText = p.model_version || 'N/A';
            
            const verdictSpan = document.getElementById('ai-verdict');
            if(p.is_phishing) {
                verdictSpan.innerText = 'MALICIOUS / PHISHING';
                verdictSpan.className = 'verdict-badge verdict-danger';
                document.getElementById('ai-result-header').innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Threat Detected';
                document.getElementById('ai-result-header').style.color = 'var(--alert-color)';
                document.getElementById('ai-result-header').style.background = 'rgba(255, 42, 85, 0.15)';
            } else {
                verdictSpan.innerText = 'SAFE';
                verdictSpan.className = 'verdict-badge verdict-safe';
                document.getElementById('ai-result-header').innerHTML = '<i class="fa-solid fa-circle-check"></i> Analysis Complete - No Threat Found';
                document.getElementById('ai-result-header').style.color = 'var(--secondary-neon)';
                document.getElementById('ai-result-header').style.background = 'rgba(176, 38, 255, 0.15)';
            }
            
            resultContainer.classList.remove('hidden');
        } else {
            alert('Error analyzing URL: ' + (data.error || 'Unknown error'));
        }
    } catch(e) {
        alert('Server unreachable');
        console.error(e);
    } finally {
        btn.innerHTML = ogText;
        btn.disabled = false;
    }
}