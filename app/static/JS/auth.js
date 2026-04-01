// 1. Select the main outer container (the one with the 'auth-container' class)
const authContainer = document.querySelector('.auth-container'); 
const overlayBtn = document.getElementById('overlayBtn');
const loginLink = document.querySelector(".signup-container a");
const registerLink = document.querySelector(".login-container a");

// Use ONE constant for the class name to avoid typos
const activeClass = "right__panel__active";

// 2. The Main Toggle Button
overlayBtn.addEventListener('click', () => {
    // Add the class to the PARENT, not the overlay itself
    authContainer.classList.toggle(activeClass);

    // Update button text based on the PARENT state
    if (authContainer.classList.contains(activeClass)) {
        overlayBtn.innerText = 'LOG IN';
    } else {
        overlayBtn.innerText = 'REGISTER';
    }
});

// 3. The Links (if you still want them to work)
loginLink.addEventListener('click', (e) => {
    e.preventDefault();
    authContainer.classList.add(activeClass);
    overlayBtn.innerText = 'Log In'; // Sync the ghost button text
});

registerLink.addEventListener('click', (e) => {
    e.preventDefault();
    authContainer.classList.remove(activeClass);
    overlayBtn.innerText = 'Register here'; // Sync the ghost button text
});