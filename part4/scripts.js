let allPlaces = []; // Store all fetched places for filtering

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for(let i=0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }
}

async function fetchPlaces(token) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        const response = await fetch('http://localhost:5000/places', { // Assuming API endpoint for places
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            allPlaces = await response.json();
            displayPlaces(allPlaces);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            // Redirect to login if unauthorized
            if (response.status === 401) {
                window.location.href = 'login.html';
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(placesToDisplay) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = ''; // Clear existing content

    placesToDisplay.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price_per_night); // Store price for filtering

        placeCard.innerHTML = `
            <h2>${place.name}</h2>
            <p class="price-per-night">$${place.price_per_night} / night</p>
            <button class="details-button" data-place-id="${place.id}">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Login form submission logic (from previous task)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed: ' + response.statusText);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred during login. Please try again.');
            }
        });
    }

    // Check authentication and fetch places on page load
    checkAuthentication();

    // Price filter logic
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;
            const filteredPlaces = allPlaces.filter(place => {
                if (maxPrice === 'all') {
                    return true;
                } else {
                    return place.price_per_night <= parseFloat(maxPrice);
                }
            });
            displayPlaces(filteredPlaces);
        });
    }
});