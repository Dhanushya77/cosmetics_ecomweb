let passwd = document.getElementById("pass")
let len = document.getElementById("len")
let cap = document.getElementById("cap")
let sml = document.getElementById("sml")
let dig = document.getElementById("dig")
let char = document.getElementById("char")

passwd.addEventListener('input', function () {
    const password = passwd.value
    // len.style.color = password.length >= 8 ? 'green' : 'red'
    // cap.style.color = /[A-Z]/.test(password) ? 'green' : 'red'
    // sml.style.color = /[a-z]/.test(password) ? 'green' : 'red'
    // dig.style.color = /\d/.test(password) ? 'green' : 'red'
    // char.style.color = /[!@#$%&*]/.test(password) ? 'green' : 'red'
    len.style.display = password.length >= 8 ? 'none' : 'block'
    cap.style.display = /[A-Z]/.test(password) ? 'none' : 'block'
    sml.style.display = /[a-z]/.test(password) ? 'none' : 'block'
    dig.style.display = /\d/.test(password) ? 'none' : 'block'
    char.style.display = /[!@#$%&*]/.test(password) ? 'none' : 'block'
})
document.getElementById("registerForm").addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent form submission for validation
    let pwd = passwd.value;
    let messageContainer = document.createElement('div');
    messageContainer.classList.add('alert', 'alert-warning', 'alert-dismissible', 'fade', 'show');

    if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@.#$!%*?&])[A-Za-z\d@.#$!%*?&]{8,}$/.test(pwd)) {
        this.submit();  // Submit form if password is valid
    } else {
        messageContainer.innerHTML = 'Please ensure your password meets all the criteria.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
        let passwordField = document.getElementById("pass");
        passwordField.parentNode.appendChild(messageContainer);
        messageContainer.classList.add('alert', 'alert-dismissible', 'fade', 'show');
        messageContainer.style.backgroundColor = '#7e0e463b';
        messageContainer.style.color = '#7e0e46';
        messageContainer.innerHTML = 'Please ensure your password meets all the criteria.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    }
});