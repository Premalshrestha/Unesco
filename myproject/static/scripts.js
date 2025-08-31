//dashboard lai

// script.js
// Mobile menu toggle
const mobileMenuToggle = document.getElementById("mobileMenuToggle");
const navLinks = document.getElementById("navLinks");

mobileMenuToggle.addEventListener("click", () => {
  navLinks.classList.toggle("open");
});

// Smooth scrolling for navigation links
document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();

    // Remove active class from all links
    document
      .querySelectorAll(".nav-links a")
      .forEach((l) => l.classList.remove("active"));

    // Add active class to clicked link
    link.classList.add("active");

    // Close mobile menu if open
    navLinks.classList.remove("open");
  });
});

// Add hover effects to cards
document.querySelectorAll(".card").forEach((card) => {
  card.addEventListener("mouseenter", () => {
    card.style.transform = "translateY(-10px) scale(1.02)";
  });

  card.addEventListener("mouseleave", () => {
    card.style.transform = "translateY(0) scale(1)";
  });
});

// Animate progress bars on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const progressBar = entry.target.querySelector(".progress-bar div");
      if (progressBar) {
        progressBar.style.width = progressBar.style.width || "0%";
      }
    }
  });
}, observerOptions);

document.querySelectorAll(".progress").forEach((progress) => {
  observer.observe(progress);
});

// Add click animations to action buttons
document.querySelectorAll(".actions button").forEach((button) => {
  button.addEventListener("click", () => {
    button.style.transform = "scale(0.95)";
    setTimeout(() => {
      button.style.transform = "translateY(-5px) scale(1)";
    }, 100);
  });
});

// Notification bell animation
const notificationBell = document.querySelector(".notification-bell");
setInterval(() => {
  notificationBell.style.animation = "none";
  setTimeout(() => {
    notificationBell.style.animation = "float 1s ease-in-out";
  }, 10);
}, 5000);

// Welcome message personalization (simulate data from Django backend)
const welcomeData = {
  name: "Sarah",
  weeks: 24,
  trimester: "Second",
  wellness: 87,
  weightGain: 2.1,
  carePoints: 12,
};

// Update welcome message
document.querySelector(
  ".welcome h2"
).textContent = `Welcome back, ${welcomeData.name}! 👋`;
document.querySelector(
  ".welcome p"
).textContent = `You're ${welcomeData.weeks} weeks pregnant. Here's how you're doing today.`;
// End of dashboard
