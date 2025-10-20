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

	initProjectFilters();
	initTeamDirectory();
	initBackToTop();
	initScrollProgress();
	initCopyButtons();
	initContactCards();
});

function normalizeTags(value = "") {
	return value
		.split(",")
		.map((tag) => tag.trim().toLowerCase())
		.filter(Boolean);
}

function initProjectFilters() {
	const sections = document.querySelectorAll('[data-filter-scope="projects"]');
	sections.forEach((section) => {
		const chips = section.querySelectorAll(".filter-chip");
		const cards = section.querySelectorAll(".project-card");
		const emptyState = section.querySelector(".projects-empty");
		if (!chips.length || !cards.length) {
			return;
		}

		const tagCache = new Map();
		cards.forEach((card) => {
			tagCache.set(card, normalizeTags(card.dataset.tags));
		});

		const updateVisibility = (activeFilter) => {
			let visibleCount = 0;
			cards.forEach((card) => {
				const tags = tagCache.get(card) || [];
				const matches = activeFilter === "all" || tags.includes(activeFilter);
				const hidden = !matches;
				card.style.display = hidden ? "none" : "";
				card.setAttribute("aria-hidden", hidden ? "true" : "false");
				if (!hidden) {
					visibleCount += 1;
				}
			});
			if (emptyState) {
				emptyState.toggleAttribute("hidden", visibleCount > 0);
			}
		};

		const setActiveChip = (chip, filterValue) => {
			chips.forEach((candidate) => {
				const isActive = candidate === chip;
				candidate.classList.toggle("is-active", isActive);
				candidate.setAttribute("aria-pressed", isActive ? "true" : "false");
			});
			updateVisibility(filterValue);
		};

		chips.forEach((chip) => {
			chip.addEventListener("click", () => {
				const targetFilter = (chip.dataset.filter || "all").toLowerCase();
				setActiveChip(chip, targetFilter);
			});
		});

		const preset = section.querySelector(".filter-chip.is-active") || chips[0];
		const initialFilter = preset
			? (preset.dataset.filter || "all").toLowerCase()
			: "all";
		setActiveChip(preset || chips[0], initialFilter);
	});
}

function initTeamDirectory() {
	const section = document.querySelector('[data-filter-scope="team"]');
	if (!section) {
		return;
	}

	const cards = section.querySelectorAll(".project-card");
	if (!cards.length) {
		return;
	}

	const chips = section.querySelectorAll(".team-filters .filter-chip");
	if (!chips.length) {
		return;
	}
	const searchInput = document.getElementById("teamSearch");
	const emptyState = section.querySelector(".projects-empty");
	const cardMeta = new Map();

	cards.forEach((card) => {
		const tags = normalizeTags(card.dataset.tags);
		const strings = [
			card.querySelector("h2")?.textContent || "",
			card.querySelector(".project-status")?.textContent || "",
			card.dataset.wing || "",
			card.dataset.subteam || "",
			card.querySelector(".project-summary")?.textContent || "",
			card.querySelector(".project-meta")?.textContent || "",
			card.querySelector(".project-links")?.textContent || "",
		];
		cardMeta.set(card, {
			tags,
			text: strings.join(" ").toLowerCase(),
		});
	});

	let activeFilter = "all";

	const applyFilters = () => {
		const query = (searchInput?.value || "").trim().toLowerCase();
		let visibleCount = 0;
		cards.forEach((card) => {
			const meta = cardMeta.get(card) || { tags: [], text: "" };
			const matchesFilter =
				activeFilter === "all" || meta.tags.includes(activeFilter);
			const matchesQuery =
				!query ||
				meta.text.includes(query) ||
				meta.tags.some((tag) => tag.includes(query));
			const shouldShow = matchesFilter && matchesQuery;
			card.style.display = shouldShow ? "" : "none";
			card.setAttribute("aria-hidden", shouldShow ? "false" : "true");
			if (shouldShow) {
				visibleCount += 1;
			}
		});
		if (emptyState) {
			emptyState.toggleAttribute("hidden", visibleCount > 0);
		}
	};

	chips.forEach((chip) => {
		chip.addEventListener("click", () => {
			activeFilter = (chip.dataset.filter || "all").toLowerCase();
			chips.forEach((candidate) => {
				const isActive = candidate === chip;
				candidate.classList.toggle("is-active", isActive);
				candidate.setAttribute("aria-pressed", isActive ? "true" : "false");
			});
			applyFilters();
			if (searchInput) {
				searchInput.focus();
			}
		});
	});

	if (searchInput) {
		let debounceTimer;
		searchInput.addEventListener("input", () => {
			window.clearTimeout(debounceTimer);
			debounceTimer = window.setTimeout(applyFilters, 120);
		});
	}

	const presetChip =
		section.querySelector(".team-filters .filter-chip.is-active") || chips[0];
	activeFilter = presetChip
		? (presetChip.dataset.filter || "all").toLowerCase()
		: "all";
	chips.forEach((chip) => {
		const isActive = chip === presetChip;
		chip.setAttribute("aria-pressed", isActive ? "true" : "false");
		chip.classList.toggle("is-active", isActive);
	});
	applyFilters();
}

function initBackToTop() {
	const button = document.getElementById("backToTop");
	if (!button) {
		return;
	}

	const toggleVisibility = () => {
		const shouldShow = window.scrollY > 320;
		button.classList.toggle("visible", shouldShow);
	};

	button.addEventListener("click", () => {
		window.scrollTo({ top: 0, behavior: "smooth" });
	});

	window.addEventListener("scroll", toggleVisibility, { passive: true });
	toggleVisibility();
}

function initScrollProgress() {
	const progress = document.getElementById("scrollProgress");
	if (!progress) {
		return;
	}

	const updateProgress = () => {
		const scrollTop = window.scrollY || document.documentElement.scrollTop;
		const scrollHeight =
			document.documentElement.scrollHeight - window.innerHeight;
		const ratio = scrollHeight > 0 ? scrollTop / scrollHeight : 0;
		progress.style.transform = `scaleX(${ratio})`;
		progress.setAttribute("data-progress", Math.round(ratio * 100));
	};

	window.addEventListener("scroll", updateProgress, { passive: true });
	window.addEventListener("resize", updateProgress);
	updateProgress();
}

function initCopyButtons() {
	const buttons = document.querySelectorAll("[data-copy-value]");
	if (!buttons.length || !navigator.clipboard) {
		return;
	}

	buttons.forEach((button) => {
		button.addEventListener("click", async () => {
			const value = button.getAttribute("data-copy-value") || "";
			if (!value) return;
			try {
				await navigator.clipboard.writeText(value);
				button.classList.add("is-copied");
				setTimeout(() => button.classList.remove("is-copied"), 1400);
			} catch (error) {
				console.error("Clipboard copy failed", error);
			}
		});
	});
}

function initContactCards() {
	const forms = document.querySelectorAll(".contact-card[data-email]");
	if (!forms.length) {
		return;
	}

	forms.forEach((form) => {
		form.addEventListener("submit", (event) => {
			event.preventDefault();
			const target = event.currentTarget;
			if (!(target instanceof HTMLFormElement)) {
				return;
			}
			const email = target.dataset.email;
			if (!email) {
				return;
			}
			const nameInput = target.querySelector("input[name='name']");
			const messageInput = target.querySelector("textarea[name='message']");
			const name = nameInput ? nameInput.value.trim() : "";
			const message = messageInput ? messageInput.value.trim() : "";
			const subject = encodeURIComponent(
				`NSA Inquiry from ${name || "Prospective Member"}`
			);
			const bodyParts = [];
			if (name) bodyParts.push(`Name: ${name}`);
			if (message) bodyParts.push("\n" + message);
			const body = encodeURIComponent(bodyParts.join("\n"));
			window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
		});
	});
}

// === FAQ Toggle ===
function toggleFaq(button) {
	const answer = button.nextElementSibling;
	if (!answer) {
		return;
	}
	const isOpen = answer.classList.contains("open");

	// Toggle active state on button
	button.classList.toggle("active");
	button.setAttribute("aria-expanded", isOpen ? "false" : "true");

	// Toggle answer visibility
	if (isOpen) {
		answer.classList.remove("open");
		answer.setAttribute("aria-hidden", "true");
	} else {
		answer.classList.add("open");
		answer.setAttribute("aria-hidden", "false");
	}
}
