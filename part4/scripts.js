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