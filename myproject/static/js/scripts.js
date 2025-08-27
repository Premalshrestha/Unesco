// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute("href")).scrollIntoView({
            behavior: "smooth"
        });
    });
});

// Hero button bounce effect
const heroButton = document.querySelector(".hero .btn");
if (heroButton) {
    heroButton.addEventListener("mouseover", () => {
        heroButton.classList.add("animate-bounce");
    });
    heroButton.addEventListener("mouseout", () => {
        heroButton.classList.remove("animate-bounce");
    });
}

// Card hover shadow & scale (additional JS fallback)
document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.transform = "scale(1.05)";
        card.style.transition = "0.3s ease-in-out";
    });
    card.addEventListener("mouseleave", () => {
        card.style.transform = "scale(1)";
    });
});

// Optional: simple alert for CTA button
heroButton.addEventListener("click", () => {
    alert("Welcome! Please login or register to start tracking your pregnancy.");
});
