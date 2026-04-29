document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const button = form.querySelector("button");

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      alert("Please fill in all fields");
      return;
    }

    button.disabled = true;
    button.textContent = "Logging in...";

    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      let data = {};

      try {
        data = await response.json();
      } catch {
        data = {};
      }

      console.log("Response status:", response.status);
      console.log("Login response data:", data);

      if (response.ok) {
        const token = data.token || data.access_token || data.access || data.jwt;
        const userId = data.user_id;

        if (!token) {
          alert("Login succeeded, but no token was returned.");
          console.log("Returned data:", data);
          return;
        }

        if (!userId) {
          alert("Login succeeded, but no user_id was returned.");
          console.log("Returned data:", data);
          return;
        }

        setCookie("token", token, 1);
        setCookie("user_id", userId, 1);

        console.log("Saved cookies:", document.cookie);

        window.location.href = "index.html";
      } else {
        alert(data.message || data.error || "Invalid email or password");
      }

    } catch (error) {
      console.error("Login error:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      button.disabled = false;
      button.textContent = "Login";
    }
  });
});

function setCookie(name, value, days) {
  let expires = "";

  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }

  document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=/`;
}