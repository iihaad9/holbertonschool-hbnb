document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded");
  updateAuthButton();
  fetchPlaces();
});

/* ============================= */
/* Fetch Places                  */
/* ============================= */

function fetchPlaces() {
  console.log("Fetching places...");

  fetch("http://127.0.0.1:5000/api/v1/places/")
    .then(response => {
      console.log("Response status:", response.status);
      return response.json();
    })
    .then(data => {
      console.log("Places data:", data);
      displayPlaces(data);
    })
    .catch(error => {
      console.error("Error fetching places:", error);
    });
}

/* ============================= */
/* Display Places                */
/* ============================= */

function displayPlaces(places) {
  const container = document.getElementById("places-list");

  if (!container) {
    console.error("places-list not found");
    return;
  }

  container.innerHTML = "";

  places.forEach(place => {
    const card = document.createElement("article");
    card.className = "place-card";

    const title = document.createElement("h2");
    title.textContent = place.title;

    const location = document.createElement("p");
    location.textContent = `Location: ${place.latitude}, ${place.longitude}`;

    const button = document.createElement("a");
    button.className = "details-button";
    button.href = `place.html?id=${place.id}`;
    button.textContent = "View Details";

    card.appendChild(title);
    card.appendChild(location);
    card.appendChild(button);

    container.appendChild(card);
  });
}

/* ============================= */
/* Auth Button Logic             */
/* ============================= */

function updateAuthButton() {
  const authBtn = document.querySelector(".login-button");

  if (!authBtn) {
    console.error("login-button not found");
    return;
  }

  const token = getCookie("token");

  if (token) {
    authBtn.textContent = "Logout";
    authBtn.href = "#";

    authBtn.addEventListener("click", (e) => {
      e.preventDefault();
      deleteCookie("token");
      window.location.reload();
    });

  } else {
    authBtn.textContent = "Login";
    authBtn.href = "login.html";
  }
}

/* ============================= */
/* Cookie Helpers                */
/* ============================= */

function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split("=");

    if (key === name) {
      return value;
    }
  }

  return null;
}

function deleteCookie(name) {
  document.cookie = name + "=; Max-Age=0; path=/";
}
/* ============================= */
/* Place Details Page            */
/* ============================= */

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('place-details')) {
    initializePlacePage();
  }
});

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

  if (token) {
    addReviewSection.style.display = 'block';
    addReviewLink.href = `add_review.html?id=${placeId}`;
  } else {
    addReviewSection.style.display = 'none';
  }
}

function fetchPlaceDetails (placeId) {
  fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch place details');
      }
      return response.json();
    })
    .then(place => {
      displayPlaceDetails(place);
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

  const title = place.title || place.name || 'Place Details';
  const price = place.price_by_night !== undefined ? place.price_by_night : 'N/A';
  const description = place.description || 'N/A';
  const host = place.owner || place.host || 'N/A';

  container.innerHTML = `
    <h1>${title}</h1>
    <div class="place-info"><strong>Host:</strong> ${host}</div>
    <div class="place-info"><strong>Price per night:</strong> $${price}</div>
    <div class="place-info"><strong>Description:</strong> ${description}</div>
  `;
}

function displayPlaceError (message) {
  const container = document.getElementById('place-details');

  if (!container) {
    return;
  }

  container.innerHTML = `<p>${message}</p>`;
}

function fetchPlaceReviews (placeId) {
  fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch reviews');
      }
      return response.json();
    })
    .then(reviews => {
      displayReviews(reviews);
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
    user.textContent = review.user || review.user_name || 'Anonymous';

    const comment = document.createElement('p');
    comment.textContent = review.text || review.comment || 'No comment';

    const rating = document.createElement('p');
    rating.textContent = `Rating: ${review.rating !== undefined ? review.rating : 'N/A'}`;

    card.appendChild(user);
    card.appendChild(comment);
    card.appendChild(rating);

    container.appendChild(card);
  });
}
