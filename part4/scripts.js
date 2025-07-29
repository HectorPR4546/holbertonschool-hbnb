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
    const addReviewLink = document.getElementById('add-review-link'); // For place.html

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            // Only fetch places if on index.html
            if (window.location.pathname.endsWith('index.html')) {
                fetchPlaces(token);
            }
        }
    }

    if (addReviewLink) {
        if (!token) {
            addReviewLink.style.display = 'none';
        } else {
            addReviewLink.style.display = 'block';
        }
    }
    return token; // Return token for use in other functions
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

        // Add event listener for View Details button
        placeCard.querySelector('.details-button').addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
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
        const response = await fetch(`http://localhost:5000/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            if (response.status === 401) {
                window.location.href = 'login.html';
            } else {
                alert('Failed to load place details.');
            }
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        alert('An error occurred while loading place details.');
    }
}

function displayPlaceDetails(place) {
    const placeDetailsContent = document.getElementById('place-details-content');
    if (!placeDetailsContent) return;

    placeDetailsContent.innerHTML = `
        <h1>${place.name}</h1>
        <div class="place-info">
            <p><strong>Host:</strong> ${place.host_name || 'N/A'}</p>
            <p><strong>Price per night:</strong> $${place.price_per_night}</p>
            <p><strong>Description:</strong> ${place.description || 'No description provided.'}</p>
            <p><strong>Amenities:</strong> ${place.amenities && place.amenities.length > 0 ? place.amenities.join(', ') : 'None'}</p>
        </div>

        <h2>Reviews</h2>
        <div class="reviews-list">
            ${place.reviews && place.reviews.length > 0 ? place.reviews.map(review => `
                <div class="review-card">
                    <p><strong>Comment:</strong> ${review.comment}</p>
                    <p><strong>User:</strong> ${review.user_name || 'Anonymous'}</p>
                    <p><strong>Rating:</strong> ${review.rating}/5</p>
                </div>
            `).join('') : '<p>No reviews yet.</p>'}
        </div>

        <a href="add_review.html?place_id=${place.id}" class="add-review-button" id="add-review-link">Add Review</a>
    `;

    // Re-check authentication for the add review link after content is loaded
    checkAuthentication();
}

async function submitReview(token, placeId, rating, comment) {
    try {
        const response = await fetch(`http://localhost:5000/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ rating: parseInt(rating), comment: comment })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            // Optionally redirect or clear form
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            alert('Failed to submit review: ' + (errorData.message || response.statusText));
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting the review. Please try again.');
    }
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

    // Check authentication and fetch data based on the current page
    const token = checkAuthentication();

    if (window.location.pathname.endsWith('index.html')) {
        // fetchPlaces is called inside checkAuthentication for index.html
    } else if (window.location.pathname.endsWith('place.html')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(token, placeId);
        } else {
            alert('Place ID not found in URL.');
            window.location.href = 'index.html'; // Redirect if no ID
        }
    } else if (window.location.pathname.endsWith('add_review.html')) {
        const reviewForm = document.getElementById('add-review-form');
        const placeId = getPlaceIdFromURL();

        if (!token) {
            window.location.href = 'index.html'; // Redirect if not authenticated
            return;
        }

        if (!placeId) {
            alert('Place ID not found for review.');
            window.location.href = 'index.html';
            return;
        }

        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();

                const rating = document.getElementById('rating').value;
                const comment = document.getElementById('comment').value;

                await submitReview(token, placeId, rating, comment);
            });
        }
    }
});