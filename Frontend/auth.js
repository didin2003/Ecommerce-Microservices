// auth.js - CLEAN VERSION (copy exactly)
const AUTH_API = 'https://auth.didin.in/api/auth';

function getToken() {
    return localStorage.getItem('access_token');
}

function isAuthenticated() {
    return !!getToken();
}

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

function redirectIfAuthenticated() {
    if (isAuthenticated()) {
        window.location.href = 'index.html';
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = 'login.html';
}

// ✅ showAlert - properly defined and exported
function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    if (!container) {
        console.warn('⚠️ alert-container not found');
        return;
    }
    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
}

// ✅ apiFetch wrapper
async function apiFetch(endpoint, options = {}) {
    const token = getToken();
    const res = await fetch(`${AUTH_API}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw data;
    return data;
}

// ✅ CRITICAL: Attach to window so inline scripts can use them
window.AUTH_API = AUTH_API;
window.showAlert = showAlert;
window.apiFetch = apiFetch;
window.requireAuth = requireAuth;
window.redirectIfAuthenticated = redirectIfAuthenticated;
window.logout = logout;

// ✅ Debug log to confirm auth.js executed
console.log('✅ auth.js loaded | AUTH_API:', AUTH_API);