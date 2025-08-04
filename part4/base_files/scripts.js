const config = {
    apiBaseUrl: 'http://localhost:5000/api/v1'
};

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
    const loginLink = document.querySelector('.login-button');
    const addReviewSection = document.querySelector('.add-review');

    // For add_review.html, redirect if not authenticated
    if (window.location.pathname.includes('add_review.html')) {
        if (!token) {
            window.location.href = 'index.html';
            return null; // Stop execution if redirecting
        }
    }

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (addReviewSection) addReviewSection.style.display = 'block';
    }

    // Fetch places for index.html
    if (document.querySelector('.place-card-container')) {
        fetchPlaces(token);
    }

    // Fetch place details for place.html
    if (document.querySelector('.place-details')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }
    }
    return token; // Return token for use in other functions
}

async function fetchPlaces(token = null) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${config.apiBaseUrl}/places/`, {
            method: 'GET',
            headers: headers,
            redirect: 'follow' 
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else if (response.status === 401) {
            // If unauthorized, clear token and show login link
            document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
            checkAuthentication();
        } else {
            console.error('Failed to fetch places:', response.statusText);
            alert('Failed to load places. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        alert('An error occurred while fetching places.');
    }
}

function displayPlaces(places) {
    const placesContainer = document.querySelector('.place-card-container');
    if (!placesContainer) return; // Ensure element exists

    placesContainer.innerHTML = ''; // Clear existing content

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price); // For filtering

        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p class="price">Price per night: $${place.price}</p>
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        placesContainer.appendChild(placeCard);
    });
    setupPriceFilter(places);
}

function setupPriceFilter(places) {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return; // Ensure element exists

    const prices = [10, 50, 100];

    // Populate dropdown options
    priceFilter.innerHTML = '';
    prices.forEach(price => {
        const option = document.createElement('option');
        option.value = price;
        option.textContent = `$${price}`;
        priceFilter.appendChild(option);
    });
    const allOption = document.createElement('option');
    allOption.value = 'all';
    allOption.textContent = 'All';
    priceFilter.appendChild(allOption);

    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach(card => {
            const placePrice = parseFloat(card.getAttribute('data-price'));
            if (selectedPrice === 'all' || placePrice <= parseFloat(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${config.apiBaseUrl}/places/${placeId}/`, { 
            method: 'GET',
            headers: headers,
            redirect: 'follow' 
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            alert('Failed to load place details. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        alert('An error occurred while fetching place details.');
    }
}

function displayPlaceDetails(place) {
    const placeDetailsContainer = document.querySelector('.place-details');
    const reviewsContainer = document.querySelector('.review-card-container');
    if (!placeDetailsContainer || !reviewsContainer) return; // Ensure elements exist

    placeDetailsContainer.innerHTML = `
        <h2>${place.title}</h2>
        <p><strong>Description:</strong> ${place.description}</p>
        <p><strong>Price per night:</strong> $${place.price}</p>
        <p><strong>Owner:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
        <h3>Amenities:</h3>
        <ul>
            ${place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')}
        </ul>
        <button class="btn" onclick="window.location.href='add_review.html?place_id=${place.id}'">Add Review</button>
    `;

    reviewsContainer.innerHTML = ''; // Clear existing reviews
    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            reviewCard.innerHTML = `
                <h3>Rating: ${review.rating}/5</h3>
                <p>${review.text}</p>
                <p><em>By User ID: ${review.user_id}</em></p>
            `;
            reviewsContainer.appendChild(reviewCard);
        });
    } else {
        reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
    }
}

async function submitReview(token, placeId, rating, comment) {
    try {
        const response = await fetch(`${config.apiBaseUrl}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ place_id: placeId, rating: parseInt(rating), text: comment, user_id: getUserIdFromToken(token) }) // Assuming user_id can be extracted from token or is known
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            // Optionally redirect or clear form
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            alert('Failed to submit review: ' + (errorData.error || response.statusText));
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting review. Please try again.');
    }
}

// Helper to get user ID from token (simplified for demonstration)
function getUserIdFromToken(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload).id;
    } catch (e) {
        console.error("Error decoding token:", e);
        return null;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Login form handling (existing code)
    const loginForm = document.getElementById('login-form-fields');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${config.apiBaseUrl}/auth/login`, {
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
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.error || response.statusText));
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred during login. Please try again.');
            }
        });
    }

    // Add Review form handling
    const addReviewForm = document.getElementById('add-review-form-fields');
    if (addReviewForm) {
        const token = checkAuthentication(); // This will redirect if not authenticated
        const placeId = getPlaceIdFromURL();

        if (token && placeId) { // Only proceed if authenticated and placeId is available
            addReviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const rating = document.getElementById('rating').value;
                const comment = document.getElementById('comment').value;
                await submitReview(token, placeId, rating, comment);
            });
        }
    }

    // Call checkAuthentication on all pages to manage login link visibility and fetch data if authenticated
    checkAuthentication();
});