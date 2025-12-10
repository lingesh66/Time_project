/**
 * Time Management Calculator - Frontend JavaScript
 * Handles user interactions and API communication
 */

// Configuration
const CONFIG = {
    // Change this to your deployed backend URL
    API_URL: 'https://time-project-3.onrender.com',
    // For production, use your deployed backend:
    // API_URL: 'https://your-backend.onrender.com'
};

// Sample data for testing
const SAMPLE_DATA = `104138	Lingesh Balamurugan	10-12-2025	10-12-2025 10:14:29	LD CHN-1 (ASC) IN - 1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:51:32	LD CHN-1 (ASC) Cafeteria IN-1	Exit Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:51:48	LD CHN-1 (ASC) Cafeteria OUT-1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:52:13	LD CHN-1 (ASC) Cafeteria IN-2	Exit Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 12:54:45	LD CHN-1 (ASC) Cafeteria OUT-1	Entry Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 13:16:30	LD CHN-1 (ASC) Cafeteria IN-2	Exit Granted
104138	Lingesh Balamurugan	10-12-2025	10-12-2025 13:32:26	LD CHN-1 (ASC) Cafeteria OUT-2	Entry Granted`;

// DOM Elements
const logInput = document.getElementById('logInput');
const calculateBtn = document.getElementById('calculateBtn');
const clearBtn = document.getElementById('clearBtn');
const sampleBtn = document.getElementById('sampleBtn');
const emptyState = document.getElementById('emptyState');
const resultsContent = document.getElementById('resultsContent');
const loadingOverlay = document.getElementById('loadingOverlay');

// Event Listeners
calculateBtn.addEventListener('click', handleCalculate);
clearBtn.addEventListener('click', handleClear);
sampleBtn.addEventListener('click', handleLoadSample);

// Handle calculate button click
async function handleCalculate() {
    const logs = logInput.value.trim();

    if (!logs) {
        showNotification('Please paste your time logs first', 'error');
        return;
    }

    try {
        showLoading(true);
        const result = await calculateLogoutTime(logs);
        displayResults(result);
        showNotification('Calculation completed successfully!', 'success');
    } catch (error) {
        console.error('Calculation error:', error);
        displayError(error.message || 'Failed to calculate. Please check your input.');
        showNotification(error.message || 'Failed to calculate. Please check your input.', 'error');
    } finally {
        showLoading(false);
    }
}

// Handle clear button click
function handleClear() {
    logInput.value = '';
    hideResults();
    showNotification('Input cleared', 'info');
}

// Handle load sample button click
function handleLoadSample() {
    logInput.value = SAMPLE_DATA;
    showNotification('Sample data loaded', 'success');
}

// API call to calculate logout time with timeout and retry
async function calculateLogoutTime(logs) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 90000); // 90 second timeout

    try {
        const response = await fetch(`${CONFIG.API_URL}/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ logs }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Server error' }));
            throw new Error(error.detail || 'Calculation failed');
        }

        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);

        if (error.name === 'AbortError') {
            throw new Error('Request timed out. The backend might be waking up (Render free tier). Please try again in a moment.');
        }

        if (error.message.includes('Failed to fetch')) {
            throw new Error('Cannot connect to backend. Please check if the backend is deployed and running at: ' + CONFIG.API_URL);
        }

        throw error;
    }
}

// Display results
function displayResults(data) {
    emptyState.classList.add('hidden');
    resultsContent.classList.remove('hidden');

    const statusColor = data.status === 'completed' ? 'green' : 'blue';
    const statusText = data.status === 'completed' ? 'Completed' : 'In Progress';

    resultsContent.innerHTML = `
        <!-- Employee Info -->
        <div class="result-card bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-xl p-6 border border-blue-500/20">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-blue-300">Employee Information</h3>
                <span class="px-3 py-1 bg-${statusColor}-500/20 text-${statusColor}-300 rounded-full text-sm font-medium">
                    ${statusText}
                </span>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <p class="text-gray-400 text-sm">Employee ID</p>
                    <p class="text-white font-semibold">${data.employee_id}</p>
                </div>
                <div>
                    <p class="text-gray-400 text-sm">Name</p>
                    <p class="text-white font-semibold">${data.name}</p>
                </div>
                <div class="col-span-2">
                    <p class="text-gray-400 text-sm">Date</p>
                    <p class="text-white font-semibold">${formatDate(data.date)}</p>
                </div>
            </div>
        </div>

        <!-- Time Details -->
        <div class="result-card bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-xl p-6 border border-purple-500/20">
            <h3 class="text-lg font-semibold text-purple-300 mb-4">Time Details</h3>
            <div class="space-y-3">
                <div class="flex justify-between items-center">
                    <span class="text-gray-400">First IN</span>
                    <span class="text-white font-semibold">${formatTime(data.first_in)}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-400">Last OUT</span>
                    <span class="text-white font-semibold">${data.last_out ? formatTime(data.last_out) : 'Still in office'}</span>
                </div>
                <div class="h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent"></div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-400">Cafeteria Time</span>
                    <span class="text-orange-300 font-semibold">${data.total_cafeteria_duration}</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-400">Net In-Office Time</span>
                    <span class="text-green-300 font-semibold">${data.net_in_office_duration}</span>
                </div>
            </div>
        </div>

        <!-- Expected Logout -->
        <div class="result-card bg-gradient-to-br from-green-500/10 to-emerald-500/10 rounded-xl p-6 border border-green-500/20">
            <h3 class="text-lg font-semibold text-green-300 mb-4">Expected Logout</h3>
            <div class="text-center">
                <div class="text-4xl font-bold text-white mb-2">
                    ${data.expected_logout ? formatTime(data.expected_logout) : 'N/A'}
                </div>
                ${data.required_seconds_for_8_hours > 0 ? `
                    <p class="text-gray-400 text-sm mb-3">
                        ${data.remaining_duration} remaining to complete 8 hours
                    </p>
                    <div class="w-full bg-slate-700/50 rounded-full h-2">
                        <div class="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full transition-all duration-500" 
                             style="width: ${calculateProgress(data.net_in_office_seconds)}%"></div>
                    </div>
                    <p class="text-gray-500 text-xs mt-2">${calculateProgress(data.net_in_office_seconds).toFixed(1)}% completed</p>
                ` : `
                    <div class="flex items-center justify-center space-x-2 text-green-400">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        <span class="font-semibold">8 hours completed!</span>
                    </div>
                `}
            </div>
        </div>

        <!-- Summary Stats -->
        <div class="result-card grid grid-cols-3 gap-4 bg-slate-800/30 rounded-xl p-6 border border-slate-700/50">
            <div class="text-center">
                <p class="text-gray-400 text-xs mb-1">Total Time</p>
                <p class="text-white font-bold text-lg">${formatSeconds(data.net_in_office_seconds + data.total_cafeteria_seconds)}</p>
            </div>
            <div class="text-center border-l border-r border-slate-700/50">
                <p class="text-gray-400 text-xs mb-1">Work Time</p>
                <p class="text-green-400 font-bold text-lg">${formatSeconds(data.net_in_office_seconds)}</p>
            </div>
            <div class="text-center">
                <p class="text-gray-400 text-xs mb-1">Break Time</p>
                <p class="text-orange-400 font-bold text-lg">${formatSeconds(data.total_cafeteria_seconds)}</p>
            </div>
        </div>
    `;
}

// Hide results
function hideResults() {
    emptyState.classList.remove('hidden');
    resultsContent.classList.add('hidden');
}

// Display error in results area
function displayError(message) {
    emptyState.classList.add('hidden');
    resultsContent.classList.remove('hidden');

    resultsContent.innerHTML = `
        <div class="result-card bg-gradient-to-br from-red-500/10 to-pink-500/10 rounded-xl p-8 border border-red-500/20 text-center">
            <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            </div>
            <h3 class="text-xl font-bold text-red-300 mb-3">Calculation Failed</h3>
            <p class="text-gray-300 mb-6">${message}</p>
            <div class="space-y-2 text-sm text-gray-400">
                <p><strong>Common solutions:</strong></p>
                <ul class="list-disc list-inside space-y-1">
                    <li>Wait 10 seconds and try again (backend might be waking up)</li>
                    <li>Check if backend is running: <a href="${CONFIG.API_URL}/health" target="_blank" class="text-purple-400 hover:text-purple-300">Test Backend</a></li>
                    <li>Verify your log format matches the expected format</li>
                </ul>
            </div>
        </div>
    `;
}

// Show/hide loading overlay
function showLoading(show) {
    if (show) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const colors = {
        success: 'from-green-500 to-emerald-600',
        error: 'from-red-500 to-pink-600',
        info: 'from-blue-500 to-purple-600'
    };

    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 bg-gradient-to-r ${colors[type]} text-white px-6 py-4 rounded-xl shadow-2xl transform transition-all duration-300 translate-x-0`;
    notification.innerHTML = `
        <div class="flex items-center space-x-3">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                ${type === 'success' ?
            '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>' :
            type === 'error' ?
                '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>' :
                '<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>'
        }
            </svg>
            <span class="font-semibold">${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Utility functions
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(timeStr) {
    if (!timeStr) return 'N/A';
    const date = new Date(timeStr);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });
}

function formatSeconds(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
}

function calculateProgress(netSeconds) {
    const requiredSeconds = 8 * 3600; // 8 hours
    return Math.min((netSeconds / requiredSeconds) * 100, 100);
}

// Initialize
console.log('Time Management Calculator initialized');
console.log('API URL:', CONFIG.API_URL);
