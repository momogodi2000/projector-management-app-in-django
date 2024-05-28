const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const forgotPasswordLink = document.getElementById('forgotPasswordLink');
const forgotPasswordContainer = document.getElementById('forgotPasswordContainer');

signUpButton.addEventListener('click', () => {
    container.classList.add('right-panel-active');
});

signInButton.addEventListener('click', () => {
    container.classList.remove('right-panel-active');
});

forgotPasswordLink.addEventListener('click', (e) => {
    e.preventDefault();
    container.style.display = 'none';
    forgotPasswordContainer.style.display = 'flex';
});
