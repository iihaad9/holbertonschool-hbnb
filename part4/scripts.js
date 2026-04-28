document.addEventListener('DOMContentLoaded', () => {
  updateAuthButton();

  if (document.getElementById('places-list')) {
    fetchPlaces();
  }

  if (document.getElementById('place-details')) {
    initializePlacePage();
  }

  if (document.getElementById('review-form')) {
    initializeAddReviewPage();
  }
});

/* ============================= */
/* Places List Page              */
/* ============================= */

function fetchPlaces () {
  fetch('http://127.0.0.1:5000/api/v1/places/')
    .then(response => response.json())
    .then(data => displayPlaces(data))
    .catch(error => console.error('Error fetching places:', error));
}

function displayPlaces (places) {
  const container = document.getElementById('places-list');

  if (!container) {
    return;
  }

  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('article');
    card.className = 'place-card';

    card.innerHTML = `
      <h2>${place.title || 'Untitled Place'}</h2>
      <p>Price per night: $${place.price ?? 'N/A'}</p>
      <p>Location: ${
        place.latitude !== undefined && place.longitude !== undefined
          ? `${place.latitude}, ${place.longitude}`
          : 'N/A'
      }</p>
      <a class="details-button" href="place.html?id=${encodeURIComponent(place.id)}">
        View Details
      </a>
    `;

    container.appendChild(card);
  });
}

/* ============================= */
/* Place Details Page            */
/* ============================= */

function initializePlacePage () {
  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    displayPlaceError('Place not found.');
    return;
  }

  const token = getCookie('token');

  toggleAddReviewSection(token, placeId);
  fetchPlaceDetails(placeId);
  fetchPlaceReviews(placeId);
}

function getPlaceIdFromURL () {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function toggleAddReviewSection (token, placeId) {
  const section = document.getElementById('add-review');
  const link = document.getElementById('add-review-link');

  if (!section || !link) {
    return;
  }

  if (token) {
    section.style.display = 'block';
    link.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
  } else {
    section.style.display = 'none';
    link.href = '#';
  }
}

function fetchPlaceDetails (placeId) {
  fetch(`http://127.0.0.1:5000/api/v1/places/${encodeURIComponent(placeId)}`)
    .then(response => response.json())
    .then(place => {
      displayPlaceDetails(place);
      displayAmenities(place.amenities);
    })
    .catch(error => {
      console.error('Error fetching place details:', error);
      displayPlaceError('Failed to load place details.');
    });
}

function displayPlaceDetails (place) {
  const container = document.getElementById('place-details');

  if (!container) {
    return;
  }

  container.innerHTML = `
    <h1>${place.title || 'Place Details'}</h1>

    <div class="place-info">
      <strong>Host:</strong> ${place.owner_id || 'N/A'}
    </div>

    <div class="place-info">
      <strong>Price per night:</strong> $${place.price ?? 'N/A'}
    </div>

    <div class="place-info">
      <strong>Description:</strong> ${place.description || 'N/A'}
    </div>

    <div class="place-info">
      <strong>Location:</strong> ${
        place.latitude !== undefined && place.longitude !== undefined
          ? `${place.latitude}, ${place.longitude}`
          : 'N/A'
      }
    </div>
  `;
}

function displayAmenities (amenities) {
  const container = document.getElementById('amenities-list');

  if (!container) {
    return;
  }

  if (!Array.isArray(amenities) || amenities.length === 0) {
    container.innerHTML = '<p>No amenities available.</p>';
    return;
  }

  container.innerHTML = '';

  amenities.forEach(amenity => {
    const name = amenity.name || amenity.id || 'Unknown amenity';

    const item = document.createElement('div');
    item.className = 'amenity';

    const icon = document.createElement('img');
    icon.className = 'amenity-icon';
    icon.src = getAmenityIcon(name);
    icon.alt = `${name} icon`;

    const text = document.createElement('span');
    text.textContent = name;

    item.appendChild(icon);
    item.appendChild(text);

    container.appendChild(item);
  });
}

function getAmenityIcon (name) {
  const value = name.toLowerCase();

  if (value.includes('wifi') || value.includes('wi-fi')) {
    return 'images/wifi.png';
  }

  if (value.includes('pool')) {
    return 'images/pool.png';
  }

  if (value.includes('parking')) {
    return 'images/parking.png';
  }

  if (value.includes('pet')) {
    return 'images/pets.png';
  }

  return 'images/amenity.png';
}

function displayPlaceError (message) {
  const detailsContainer = document.getElementById('place-details');
  const amenitiesContainer = document.getElementById('amenities-list');

  if (detailsContainer) {
    detailsContainer.innerHTML = `<p>${message}</p>`;
  }

  if (amenitiesContainer) {
    amenitiesContainer.innerHTML = '';
  }
}

/* ============================= */
/* Reviews                       */
/* ============================= */

function fetchPlaceReviews (placeId) {
  fetch('http://127.0.0.1:5000/api/v1/reviews/')
    .then(response => response.json())
    .then(reviews => {
      const filteredReviews = reviews.filter(review => review.place_id === placeId);
      displayReviews(filteredReviews);
    })
    .catch(error => {
      console.error('Error fetching reviews:', error);
      displayReviews([]);
    });
}

function displayReviews (reviews) {
  const container = document.getElementById('reviews-list');

  if (!container) {
    return;
  }

  container.innerHTML = '';

  if (!reviews || reviews.length === 0) {
    container.innerHTML = '<p>No reviews yet.</p>';
    return;
  }

  reviews.forEach(review => {
    const card = document.createElement('article');
    card.className = 'review-card';

    card.innerHTML = `
      <h3>${review.user_id || 'Anonymous'}</h3>
      <p>${review.text || 'No comment'}</p>
      <p>Rating: ${review.rating ?? 'N/A'}</p>
    `;

    container.appendChild(card);
  });
}

/* ============================= */
/* Add Review Page               */
/* ============================= */

function initializeAddReviewPage () {
  const token = getCookie('token');

  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    alert('Place not found.');
    window.location.href = 'index.html';
    return;
  }

  const form = document.getElementById('review-form');

  if (!form) {
    return;
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();

    const reviewText = document.getElementById('review').value.trim();
    const rating = document.getElementById('rating').value;

    if (!reviewText || !rating) {
      alert('Please fill all fields');
      return;
    }

    await submitReview(token, placeId, reviewText, rating);
  });
}

async function submitReview (token, placeId, reviewText, rating) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        text: reviewText,
        rating: parseInt(rating),
        user_id: '1',
        place_id: placeId
      })
    });

    const data = await response.json();

    if (response.ok) {
      alert('Review submitted successfully!');
      window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
    } else {
      console.log('Review error:', data);
      alert(data.error || data.message || 'Failed to submit review');
    }
  } catch (error) {
    console.error('Error submitting review:', error);
    alert('Error submitting review');
  }
}

/* ============================= */
/* Auth Button Logic             */
/* ============================= */

function updateAuthButton () {
  const authBtn = document.querySelector('.login-button');

  if (!authBtn) {
    return;
  }

  const token = getCookie('token');

  if (token) {
    authBtn.textContent = 'Logout';
    authBtn.href = '#';

    authBtn.onclick = function (event) {
      event.preventDefault();
      deleteCookie('token');
      window.location.href = 'index.html';
    };
  } else {
    authBtn.textContent = 'Login';
    authBtn.href = 'login.html';
  }
}

/* ============================= */
/* Cookie Helpers                */
/* ============================= */

function getCookie (name) {
  const cookies = document.cookie.split(';');

  for (const cookie of cookies) {
    const [key, value] = cookie.trim().split('=');

    if (key === name) {
      return decodeURIComponent(value);
    }
  }

  return null;
}

function setCookie (name, value) {
  document.cookie = `${name}=${encodeURIComponent(value)}; path=/`;
}

function deleteCookie (name) {
  document.cookie = `${name}=; Max-Age=0; path=/`;
}