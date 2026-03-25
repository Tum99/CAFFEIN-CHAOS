// Selecting the links instead of the submit buttons
const loginLink = document.querySelector(".signup-container a");
const registerLink = document.querySelector(".login-container a");
const authContainer = document.getElementById('auth-container');
const overlayBtn = document.getElementById('overlayBtn')

overlayBtn.addEventListener('click', () => {
    authContainer.classList.toggle('right__panel__active')
})

loginLink.addEventListener('click', (e) => {
    e.preventDefault(); // Stops the page from refreshing/redirecting
    authContainer.classList.add("right-panel-active");
});

registerLink.addEventListener('click', (e) => {
    e.preventDefault(); // Stops the page from refreshing/redirecting
    authContainer.classList.remove("right-panel-active");
});