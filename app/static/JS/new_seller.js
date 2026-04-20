/* cursor */
const cur=document.getElementById('cursor'),ring=document.getElementById('cursorRing');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;cur.style.left=mx+'px';cur.style.top=my+'px';});
(function loop(){rx+=(mx-rx)*0.12;ry+=(my-ry)*0.12;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(loop);})();

/* section switching */
const sections = ['overview','farm-profile','messages','settings'];

function showSection(name, e) {
if(e) e.preventDefault();
sections.forEach(s => {
    const el = document.getElementById(`sec-${s}`);
    if(el) el.style.display = s === name ? 'block' : 'none';
});
document.querySelectorAll('.sidebar-link:not(.locked)').forEach(l => l.classList.remove('active'));
if(e && e.currentTarget) e.currentTarget.classList.add('active');
}

/* progress tracking */
let stepsComplete = 0;

function updateProgress() {
const pct = Math.round((stepsComplete / 3) * 100);
document.getElementById('progressBar').style.width = pct + '%';
document.getElementById('progressPct').textContent = pct + '%';
document.getElementById('stepsCount').textContent = stepsComplete;
}

/* complete farm profile — unlock step 2 */
function completeFarmProfile() {
// Mark step 1 done
const s1 = document.getElementById('step1');
s1.classList.remove('active-step');
s1.classList.add('completed');
document.getElementById('step1Status').className = 'step-status done';
document.getElementById('step1Status').textContent = '✓ Done';
document.getElementById('step1Btn').className = 'step-cta done-btn';
document.getElementById('step1Btn').textContent = '✓ Profile Saved';
document.getElementById('farmBadge').style.display = 'flex';

// Unlock step 2
const s2 = document.getElementById('step2');
s2.classList.remove('locked-step');
s2.classList.add('active-step');
document.getElementById('step2Status').className = 'step-status next';
document.getElementById('step2Status').textContent = '→ Up Next';
document.getElementById('step2Btn').className = 'step-cta green';
document.getElementById('step2Btn').textContent = 'Add First Listing →';

// Unlock listings in sidebar
['listingsLink','newListingLink'].forEach(id => {
    const el = document.getElementById(id);
    el.classList.remove('locked');
    el.querySelector('.sidebar-lock').remove();
});

stepsComplete = 1;
updateProgress();

// Go back to overview to show progress
showSection('overview', null);

// Scroll to setup steps
setTimeout(() => {
    document.querySelector('.setup-section').scrollIntoView({ behavior:'smooth', block:'center' });
}, 300);
}

/* logout overlay */
function openLogout() { document.getElementById('logoutOverlay').classList.add('open'); }
function closeLogout() { document.getElementById('logoutOverlay').classList.remove('open'); }
document.getElementById('logoutOverlay').addEventListener('click', function(e) {
if(e.target === this) closeLogout();
});
document.addEventListener('keydown', e => { if(e.key==='Escape') closeLogout(); });

/* init */
updateProgress();

/* staggered reveal */
const obs = new IntersectionObserver(entries => {
entries.forEach(e => {
    if(e.isIntersecting) { e.target.style.opacity='1'; e.target.style.transform='translateY(0)'; }
});
}, {threshold:0.08});
document.querySelectorAll('.setup-step,.stat-card,.zero-panel').forEach((el,i) => {
el.style.opacity='0'; el.style.transform='translateY(20px)';
el.style.transition=`opacity 0.5s ease ${i*0.07}s, transform 0.5s cubic-bezier(0.22,1,0.36,1) ${i*0.07}s`;
obs.observe(el);
});