document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Simulate API call for testing
            if (email === 'test@example.com' && password === 'password') {
                // Simulate successful login
                document.cookie = `token=fake-jwt-token; path=/`;
                alert('Login successful!');
                window.location.href = 'index.html';
            } else {
                // Simulate failed login
                alert('Login failed: Invalid credentials');
            }
        });
    }
});