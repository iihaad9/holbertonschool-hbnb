console.log("scripts loaded");
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded");
  fetchPlaces();
});

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

function displayPlaces(places) {
  const container = document.getElementById("places-list");
  console.log("Container:", container);
  console.log("Places count:", places.length);

  container.innerHTML = "";

  places.forEach(place => {
    const card = document.createElement("article");
    card.className = "place-card";

    card.innerHTML = `
      <h2>${place.title}</h2>
      <p>Location: ${place.latitude}, ${place.longitude}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    container.appendChild(card);
  });
}