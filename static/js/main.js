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

		const accent = isDark ? "#a855f7" : "#7c3aed";
		const link = isDark ? "#c084fc" : "#8b5cf6";

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
						const delay = entry.target.dataset.delay;
						if (delay) {
							entry.target.style.setProperty("--delay", delay);
						}
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
	initAccessConsole();
	initParallaxCards();
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
	// Chips might be removed, so we don't return early if they are missing

	const searchInput = document.getElementById("teamSearch");
	const emptyState = section.querySelector(".projects-empty");
	const cardMeta = new Map();

	cards.forEach((card) => {
		const tags = normalizeTags(card.dataset.tags);
		const strings = [
			card.querySelector("h3")?.textContent || "", // Changed from h2 to h3 based on new template
			card.querySelector(".member-role")?.textContent || "",
			card.dataset.wing || "",
			card.dataset.subteam || "",
			card.querySelector(".member-bio")?.textContent || "", // Added bio search
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

			if (shouldShow) {
				card.style.display = "";
				card.setAttribute("aria-hidden", "false");
				// Add animation class for live search effect
				card.classList.add("search-match");
				card.classList.remove("search-hidden");
				visibleCount += 1;
			} else {
				card.style.display = "none";
				card.setAttribute("aria-hidden", "true");
				card.classList.remove("search-match");
				card.classList.add("search-hidden");
			}
		});
		if (emptyState) {
			emptyState.toggleAttribute("hidden", visibleCount > 0);
		}
	};

	if (chips.length) {
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
	}

	if (searchInput) {
		searchInput.addEventListener("input", () => {
			// Removed debounce for "live" feel, or keep it very short
			applyFilters();
		});
	}

	if (chips.length) {
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
	}

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

function initAccessConsole() {
	const section = document.querySelector(".access-console");
	if (!section) return;

	const status = section.querySelector("[data-auth-status]");
	const providerButtons = section.querySelectorAll("[data-auth-provider]");
	const passkeyButton = section.querySelector("[data-passkey-button]");

	if (providerButtons.length) {
		providerButtons.forEach((button) => {
			button.addEventListener("click", async () => {
				const provider = button.dataset.authProvider || "provider";
				providerButtons.forEach((candidate) =>
					candidate.classList.remove("is-loading")
				);
				button.classList.add("is-loading");
				if (status) {
					const providerName =
						button.querySelector(".provider-name")?.textContent || provider;
					status.textContent = `Contacting ${providerName} for secure redirect …`;
				}
				try {
					const response = await fetch(`/auth/provider/${provider}`, {
						method: "POST",
						headers: { "Content-Type": "application/json" },
						body: JSON.stringify({
							timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
						}),
					});
					const payload = await response.json();
					const providerName =
						button.querySelector(".provider-name")?.textContent || provider;
					if (!response.ok) {
						throw new Error(payload.message || "Auth failed");
					}
					if (status) {
						status.textContent =
							payload.message || `Redirect ready for ${providerName}.`;
					}
					if (payload.redirect) {
						button.setAttribute("data-redirect", payload.redirect);
					}
				} catch (error) {
					console.error("OAuth stub error", error);
					if (status) {
						status.textContent = `Handshake failed: ${
							error.message || "try again"
						}`;
					}
				} finally {
					button.classList.remove("is-loading");
				}
			});
		});
	}

	if (passkeyButton) {
		const originalLabel =
			passkeyButton.dataset.defaultLabel || passkeyButton.textContent;
		passkeyButton.addEventListener("click", async () => {
			passkeyButton.classList.add("is-loading");
			try {
				const response = await fetch("/auth/passkey", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ alias: navigator.userAgent }),
				});
				const payload = await response.json();
				if (!response.ok) {
					throw new Error(payload.message || "Passkey failed");
				}
				passkeyButton.classList.add("is-success");
				passkeyButton.textContent = payload.message || "Passkey ready";
				window.setTimeout(() => {
					passkeyButton.classList.remove("is-success");
					passkeyButton.textContent = originalLabel;
				}, 2200);
			} catch (error) {
				console.error("Passkey stub error", error);
				passkeyButton.textContent = error.message || "Passkey failed";
				window.setTimeout(() => {
					passkeyButton.textContent = originalLabel;
				}, 2200);
			} finally {
				passkeyButton.classList.remove("is-loading");
			}
		});
	}
}

function initParallaxCards() {
	const cards = document.querySelectorAll("[data-parallax]");
	const prefersReducedMotion = window.matchMedia(
		"(prefers-reduced-motion: reduce)"
	).matches;
	if (!cards.length || prefersReducedMotion) return;

	// Scroll-based parallax observer
	const scrollObserver = new IntersectionObserver(
		(entries) => {
			entries.forEach((entry) => {
				const card = entry.target;
				const depth = parseFloat(card.dataset.depth || "0.12");

				if (entry.isIntersecting) {
					// Add subtle scroll transform when in view
					const rect = entry.boundingClientRect;
					const progress = Math.max(
						0,
						Math.min(
							1,
							(window.innerHeight - rect.top) /
								(window.innerHeight + rect.height)
						)
					);
					const translateY = (progress - 0.5) * 20 * depth;
					card.style.setProperty("--scroll-y", `${translateY}px`);
					card.classList.add("parallax-scroll");
				} else {
					card.classList.remove("parallax-scroll");
					card.style.removeProperty("--scroll-y");
				}
			});
		},
		{ threshold: [0, 0.1, 0.5, 0.9, 1] }
	);

	cards.forEach((card) => {
		const depth = parseFloat(card.dataset.depth || "0.12");
		const maxTilt = 12 * depth;

		// Mouse/touch parallax (existing logic)
		const handleMove = (point) => {
			const rect = card.getBoundingClientRect();
			const relX = (point.clientX - (rect.left + rect.width / 2)) / rect.width;
			const relY = (point.clientY - (rect.top + rect.height / 2)) / rect.height;
			const rotateY = relX * maxTilt;
			const rotateX = relY * -maxTilt;
			card.style.transform = `perspective(1100px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(var(--scroll-y, 0px))`;
			card.classList.add("parallax-ready");
		};

		const resetTilt = () => {
			card.style.transform = card.classList.contains("parallax-scroll")
				? `translateY(var(--scroll-y, 0px))`
				: "";
			card.classList.remove("parallax-ready");
		};

		card.addEventListener("pointermove", handleMove);
		card.addEventListener("pointerleave", resetTilt);
		card.addEventListener("touchmove", (event) => {
			if (event.touches && event.touches[0]) {
				handleMove(event.touches[0]);
			}
		});
		card.addEventListener("touchend", resetTilt);

		// Observe for scroll-based parallax
		scrollObserver.observe(card);
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
