document.addEventListener("DOMContentLoaded", () => {
	const themeToggle = document.getElementById("themeToggle");
	const themeIcon = document.getElementById("themeIcon");
	const body = document.body;
	const root = document.documentElement;
	const animateTargets = document.querySelectorAll("[data-animate]");

	function destroyParticles() {
		if (window.pJSDom && window.pJSDom.length) {
			window.pJSDom.forEach((instance) => {
				if (instance && instance.pJS && instance.pJS.fn.vendors.destroypJS) {
					instance.pJS.fn.vendors.destroypJS();
				}
			});
			window.pJSDom = [];
		}
	}

	function initParticles(isDark) {
		if (typeof particlesJS === "undefined") return;
		destroyParticles();

		const accent = isDark ? "#00d9f5" : "#2563eb";
		const link = isDark ? "#00f5a0" : "#14b8a6";

		particlesJS("particles-js", {
			particles: {
				number: { value: 60, density: { enable: true, value_area: 800 } },
				color: { value: accent },
				shape: { type: "circle" },
				opacity: { value: 0.45, random: true },
				size: { value: 3, random: true },
				line_linked: {
					enable: true,
					distance: 140,
					color: link,
					opacity: 0.35,
					width: 1,
				},
				move: {
					enable: true,
					speed: 2,
					direction: "none",
					random: false,
					straight: false,
					out_mode: "out",
				},
			},
			interactivity: {
				detect_on: "canvas",
				events: {
					onhover: { enable: true, mode: "grab" },
					onclick: { enable: true, mode: "push" },
					resize: true,
				},
				modes: {
					grab: { distance: 160, line_opacity: 0.75 },
					push: { particles_nb: 3 },
				},
			},
			retina_detect: true,
		});
	}

	function setTheme(mode) {
		const nextMode = mode === "light" ? "light" : "dark";
		const isDark = nextMode === "dark";
		body.classList.toggle("dark-mode", isDark);
		body.classList.toggle("light-mode", !isDark);
		root.dataset.theme = nextMode;
		root.style.setProperty("color-scheme", isDark ? "dark" : "light");
		if (themeIcon) {
			themeIcon.classList.toggle("bi-moon-stars-fill", isDark);
			themeIcon.classList.toggle("bi-sun-fill", !isDark);
		}
		localStorage.setItem("theme", nextMode);
		initParticles(isDark);
	}

	if (themeToggle) {
		themeToggle.addEventListener("click", () => {
			const isDark = body.classList.contains("dark-mode");
			setTheme(isDark ? "light" : "dark");
		});
	}

	const savedTheme = localStorage.getItem("theme");
	setTheme(savedTheme === "light" ? "light" : "dark");

	if (animateTargets.length) {
		const observer = new IntersectionObserver(
			(entries, obs) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						entry.target.classList.add("activated");
						obs.unobserve(entry.target);
					}
				});
			},
			{ threshold: 0.15, rootMargin: "0px 0px -10% 0px" }
		);

		animateTargets.forEach((el) => observer.observe(el));
	}

	const smoothAnchors = document.querySelectorAll('a[href^="#"]');
	smoothAnchors.forEach((anchor) => {
		anchor.addEventListener("click", (event) => {
			const href = anchor.getAttribute("href");
			if (!href || href === "#") return;
			const target = document.querySelector(href);
			if (target) {
				event.preventDefault();
				target.scrollIntoView({ behavior: "smooth", block: "start" });
			}
		});
	});

	const filterChips = document.querySelectorAll(".filter-chip");
	const projectCards = document.querySelectorAll(".project-card");
	const emptyState = document.querySelector(".projects-empty");
	if (filterChips.length && projectCards.length) {
		const normalize = (value = "") =>
			value
				.split(",")
				.map((tag) => tag.trim().toLowerCase())
				.filter(Boolean);

		const updateEmptyState = () => {
			const hasVisible = Array.from(projectCards).some(
				(card) => card.style.display !== "none"
			);
			if (emptyState) {
				emptyState.toggleAttribute("hidden", hasVisible);
			}
		};

		filterChips.forEach((chip) => {
			chip.addEventListener("click", () => {
				const targetFilter = chip.dataset.filter || "all";
				filterChips.forEach((c) => {
					const isActive = c === chip;
					c.classList.toggle("is-active", isActive);
					c.setAttribute("aria-pressed", isActive ? "true" : "false");
				});
				projectCards.forEach((card) => {
					const tags = normalize(card.dataset.tags);
					const matches =
						targetFilter === "all" || tags.includes(targetFilter.toLowerCase());
					card.style.display = matches ? "" : "none";
					card.setAttribute("aria-hidden", matches ? "false" : "true");
				});
				updateEmptyState();
			});
		});

		updateEmptyState();
	}

	// Initialize countdown timer
	initCountdown();
});

// === Countdown Timer ===
function initCountdown() {
	const daysEl = document.getElementById("days");
	const hoursEl = document.getElementById("hours");
	const minutesEl = document.getElementById("minutes");
	const secondsEl = document.getElementById("seconds");
	const countdownBanner = document.querySelector(".countdown-banner");

	if (!daysEl || !hoursEl || !minutesEl || !secondsEl) return;

	// Target: October 15, 2025 at 11:00 PM PKT (UTC+5)
	// Convert to UTC: 11:00 PM PKT = 6:00 PM UTC (18:00 UTC)
	const targetDate = new Date("2025-10-15T18:00:00Z");

	function updateCountdown() {
		const now = new Date();
		const diff = targetDate - now;

		if (diff <= 0) {
			// Countdown expired
			if (countdownBanner) {
				countdownBanner.style.display = "none";
			}
			return;
		}

		const days = Math.floor(diff / (1000 * 60 * 60 * 24));
		const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
		const seconds = Math.floor((diff % (1000 * 60)) / 1000);

		daysEl.textContent = String(days).padStart(2, "0");
		hoursEl.textContent = String(hours).padStart(2, "0");
		minutesEl.textContent = String(minutes).padStart(2, "0");
		secondsEl.textContent = String(seconds).padStart(2, "0");
	}

	// Update immediately and then every second
	updateCountdown();
	setInterval(updateCountdown, 1000);
}

// === FAQ Toggle ===
function toggleFaq(button) {
	const answer = button.nextElementSibling;
	const isOpen = answer.classList.contains("open");

	// Toggle active state on button
	button.classList.toggle("active");

	// Toggle answer visibility
	if (isOpen) {
		answer.classList.remove("open");
	} else {
		answer.classList.add("open");
	}
}
