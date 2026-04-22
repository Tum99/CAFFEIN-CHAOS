/* ══════════════ CURSOR LOGIC ══════════════ */
const cur = document.getElementById('cursor'), ring = document.getElementById('cursorRing');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; if(cur) cur.style.left = mx + 'px'; if(cur) cur.style.top = my + 'px'; });
(function loop() { rx += (mx - rx) * 0.12; ry += (my - ry) * 0.12; if(ring) ring.style.left = rx + 'px'; if(ring) ring.style.top = ry + 'px'; requestAnimationFrame(loop); })();

/* ══════════════ SECTION SWITCHING ══════════════ */
const sections = ['overview', 'farm-profile', 'messages', 'settings', 'new-listing'];

function showSection(name, e) {
    if (e) e.preventDefault();
    sections.forEach(s => {
        const el = document.getElementById(`sec-${s}`);
        if (el) el.style.display = s === name ? 'block' : 'none';
    });
    document.querySelectorAll('.sidebar-link:not(.locked)').forEach(l => l.classList.remove('active'));
    if (e && e.currentTarget) e.currentTarget.classList.add('active');
}

/* ══════════════ PROGRESS TRACKING ══════════════ */
// This reads the "1" or "0" we added to the HTML data-attribute
const progressBarEl = document.getElementById('progressBar');
let stepsComplete = parseInt(progressBarEl.getAttribute('data-db-steps')) || 0;

function updateProgress() {
    const pct = Math.round((stepsComplete / 3) * 100);
    const bar = document.getElementById('progressBar');
    const pctLabel = document.getElementById('progressPct');
    const countLabel = document.getElementById('stepsCount');

    if (bar) bar.style.width = pct + '%';
    if (pctLabel) pctLabel.textContent = pct + '%';
    if (countLabel) countLabel.textContent = stepsComplete;
}

/* ══════════════ PERSISTENT UI UPDATES ══════════════ */
/**
 * This function applies all the "Green" visual states and unlocks.
 * It runs automatically if the Database says step 1 is done.
 */
function applyStep1CompletionUI() {
    // 1. Mark step 1 visually done
    const s1 = document.getElementById('step1');
    if (s1) {
        s1.classList.remove('active-step');
        s1.classList.add('completed');
        document.getElementById('step1Status').className = 'step-status done';
        document.getElementById('step1Status').textContent = '✓ Done';
        document.getElementById('step1Btn').className = 'step-cta done-btn';
        document.getElementById('step1Btn').textContent = '✓ Profile Saved';
        document.getElementById('step1Btn').setAttribute('onclick', "showSection('farm-profile', event)");
    }

    // 2. Unlock step 2
    const s2 = document.getElementById('step2');
    if (s2) {
        s2.classList.remove('locked-step');
        s2.classList.add('active-step');
        document.getElementById('step2Status').className = 'step-status next';
        document.getElementById('step2Status').textContent = '→ Up Next';
        const s2Btn = document.getElementById('step2Btn');
        s2Btn.className = 'step-cta green';
        s2Btn.textContent = 'Add First Listing →';
        // Now clicking this button goes to the listing section
        s2Btn.setAttribute('onclick', "showSection('new-listing', event)");
    }

    // 3. Show the farm badge in sidebar
    const badge = document.getElementById('farmBadge');
    if (badge) badge.style.display = 'flex';

    // 4. Unlock listings in sidebar
    ['listingsLink', 'newListingLink', 'ordersLink', 'earningsLink'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.classList.remove('locked');
            const lock = el.querySelector('.sidebar-lock');
            if (lock) lock.remove();
            
            // Map the sidebar clicks to sections
            if(id === 'newListingLink') el.setAttribute('onclick', "showSection('new-listing', event)");
        }
    });
}

/* ══════════════ LOGOUT OVERLAY ══════════════ */
function openLogout() { document.getElementById('logoutOverlay').classList.add('open'); }
function closeLogout() { document.getElementById('logoutOverlay').classList.remove('open'); }

/* ══════════════ INITIALIZATION ══════════════ */
// This runs every time the page loads
function init() {
    // If Python told us Step 1 is done, unlock everything
    if (stepsComplete >= 1) {
        applyStep1CompletionUI();
    }
    updateProgress();
}

init();

/* ══════════════ REVEAL ANIMATIONS ══════════════ */
const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
        if (e.isIntersecting) { 
            e.target.style.opacity = '1'; 
            e.target.style.transform = 'translateY(0)'; 
        }
    });
}, { threshold: 0.08 });

document.querySelectorAll('.setup-step, .stat-card, .zero-panel').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = `opacity 0.5s ease ${i * 0.07}s, transform 0.5s cubic-bezier(0.22,1,0.36,1) ${i * 0.07}s`;
    obs.observe(el);
});