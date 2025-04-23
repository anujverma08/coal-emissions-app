document.getElementById('contactForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    const feedback = document.getElementById('formFeedback');

    if (name === "" || email === "" || message === "") {
        feedback.textContent = "All fields are required!";
    } else if (!validateEmail(email)) {
        feedback.textContent = "Please enter a valid email!";
    } else {
        feedback.textContent = "Form submitted successfully!";
        feedback.style.color = "green";
        document.getElementById('contactForm').reset();
    }
});

// Email validation function
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}


