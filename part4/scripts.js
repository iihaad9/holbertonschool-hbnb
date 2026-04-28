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
/* Fetch Places                  */
/* ============================= */

function fetchPlaces () {
  fetch('http://127.0.0.1:5000/api/v1/places/')
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch places');
      }
      return response.json();
    })
    .then(data => {
      displayPlaces(data);
    })
    .catch(error => {
      console.error('Error fetching places:', error);
    });
}

/* ============================= */
/* Display Places                */
/* ============================= */

function displayPlaces (places) {
  const container = document.getElementById('places-list');

  if (!container) {
    return;
  }

  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('article');
    card.className = 'place-card';

    const title = document.createElement('h2');
    title.textContent = place.title || 'Untitled Place';

    const price = document.createElement('p');
    price.textContent = place.price !== undefined
      ? `Price per night: $${place.price}`
      : 'Price per night: N/A';

    const location = document.createElement('p');
    location.textContent =
      place.latitude !== undefined && place.longitude !== undefined
        ? `Location: ${place.latitude}, ${place.longitude}`
        : 'Location: N/A';

    const button = document.createElement('a');
    button.className = 'details-button';
    button.href = `place.html?id=${encodeURIComponent(place.id)}`;
    button.textContent = 'View Details';

    card.appendChild(title);
    card.appendChild(price);
    card.appendChild(location);
    card.appendChild(button);

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
  const addReviewSection = document.getElementById('add-review');
  const addReviewLink = document.getElementById('add-review-link');

  if (!addReviewSection || !addReviewLink) {
    return;
  }

  if (token && placeId) {
    addReviewSection.style.display = 'block';
    addReviewLink.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
  } else {
    addReviewSection.style.display = 'none';
    addReviewLink.href = '#';
  }
}

function fetchPlaceDetails (placeId) {
  fetch(`http://127.0.0.1:5000/api/v1/places/${encodeURIComponent(placeId)}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch place details');
      }
      return response.json();
    })
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

  const title = place.title || 'Place Details';
  const price = place.price !== undefined ? place.price : 'N/A';
  const description = place.description || 'N/A';
  const host = place.owner_id || 'N/A';
  const location =
    place.latitude !== undefined && place.longitude !== undefined
      ? `${place.latitude}, ${place.longitude}`
      : 'N/A';

  container.innerHTML = `
    <h1>${title}</h1>
    <div class="place-info"><strong>Host:</strong> ${host}</div>
    <div class="place-info"><strong>Price per night:</strong> $${price}</div>
    <div class="place-info"><strong>Description:</strong> ${description}</div>
    <div class="place-info"><strong>Location:</strong> ${location}</div>
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
    const item = document.createElement('div');
    item.className = 'amenity';

    const name = amenity.name || amenity.id || 'Unknown amenity';

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
  const amenityName = name.toLowerCase();

  if (amenityName.includes('wifi') || amenityName.includes('wi-fi')) {
    return 'images/wifi.png';
  }

  if (amenityName.includes('pool')) {
    return 'images/pool.png';
  }

  if (amenityName.includes('parking')) {
    return 'images/parking.png';
  }

  if (amenityName.includes('pet')) {
    return 'images/pets.png';
  }

  return 'images/amenity.png';
}

function displayPlaceError (message) {
  const container = document.getElementById('place-details');
  const amenitiesContainer = document.getElementById('amenities-list');

  if (container) {
    container.innerHTML = `<p>${message}</p>`;
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
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch reviews');
      }
      return response.json();
    })
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

    const user = document.createElement('h3');
    user.textContent = review.user_id || 'Anonymous';

    const comment = document.createElement('p');
    comment.textContent = review.text || 'No comment';

    const rating = document.createElement('p');
    rating.textContent = `Rating: ${review.rating !== undefined ? review.rating : 'N/A'}`;

    card.appendChild(user);
    card.appendChild(comment);
    card.appendChild(rating);

    container.appendChild(card);
  });
}

/* ============================= */
/* Add Review Page               */
/* ============================= */

function initializeAddReviewPage () {
  const token = getCookie('token');

  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const placeId = getPlaceIdFromURL();

  if (!placeId) {
    alert('Place not found.');
    window.location.href = 'index.html';
    return;
  }

  const reviewForm = document.getElementById('review-form');

  reviewForm.addEventListener('submit', async e => {
    e.preventDefault();

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
        place_id: placeId
      })
    });

    if (response.ok) {
      alert('Review submitted successfully!');
      window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
    } else {
      alert('Failed to submit review');
    }
  } catch (error) {
    console.error(error);
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

    authBtn.onclick = function (e) {
      e.preventDefault();
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
      return value;
    }
  }

  return null;
}

function deleteCookie (name) {
  document.cookie = `${name}=; Max-Age=0; path=/`;
}