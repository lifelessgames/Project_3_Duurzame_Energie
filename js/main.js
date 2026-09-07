"use strict";

/**
 * RHE Online — main.js
 * Vanilla JS only. No external dependencies, no eval/innerHTML with
 * unsanitized input, no inline event handlers in the HTML.
 */

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  initFooterYear();
  initScrollReveal();
  initStatCounters();
  initProjectFilter();
  initContactForm();
  initHeaderShadowOnScroll();
});

/* ---------------------------------------------------------------------- */
/* Mobile navigation                                                       */
/* ---------------------------------------------------------------------- */
function initNav() {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".main-nav");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
    document.body.style.overflow = isOpen ? "hidden" : "";
  });

  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && nav.classList.contains("is-open")) {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }
  });
}

/* ---------------------------------------------------------------------- */
/* Footer year                                                             */
/* ---------------------------------------------------------------------- */
function initFooterYear() {
  const el = document.getElementById("current-year");
  if (el) el.textContent = String(new Date().getFullYear());
}

/* ---------------------------------------------------------------------- */
/* Scroll reveal animations                                                */
/* ---------------------------------------------------------------------- */
function initScrollReveal() {
  const items = document.querySelectorAll(".reveal");
  if (!items.length) return;

  if (!("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -60px 0px" }
  );

  items.forEach((el) => observer.observe(el));
}

/* ---------------------------------------------------------------------- */
/* Animated stat counters                                                  */
/* ---------------------------------------------------------------------- */
function initStatCounters() {
  const counters = document.querySelectorAll("[data-count-to]");
  if (!counters.length) return;

  const animate = (el) => {
    const target = Number(el.getAttribute("data-count-to")) || 0;
    const suffix = el.getAttribute("data-suffix") || "";
    const duration = 1400;
    const start = performance.now();

    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.round(target * eased);
      el.textContent = value.toLocaleString("nl-NL") + suffix;
      if (progress < 1) requestAnimationFrame(step);
    };

    requestAnimationFrame(step);
  };

  if (!("IntersectionObserver" in window)) {
    counters.forEach(animate);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  counters.forEach((el) => observer.observe(el));
}

/* ---------------------------------------------------------------------- */
/* Project filter (projecten.html)                                         */
/* ---------------------------------------------------------------------- */
function initProjectFilter() {
  const buttons = document.querySelectorAll("[data-filter]");
  const cards = document.querySelectorAll("[data-category]");
  if (!buttons.length || !cards.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      btn.setAttribute("aria-pressed", "true");
      buttons.forEach((b) => {
        if (b !== btn) b.setAttribute("aria-pressed", "false");
      });

      const filter = btn.getAttribute("data-filter");
      cards.forEach((card) => {
        const category = card.getAttribute("data-category");
        const show = filter === "all" || filter === category;
        card.style.display = show ? "" : "none";
      });
    });
  });
}

/* ---------------------------------------------------------------------- */
/* Contact form validation                                                 */
/* ---------------------------------------------------------------------- */
function initContactForm() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const status = document.getElementById("form-status");

  const validators = {
    name: (value) => value.trim().length >= 2,
    email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim()),
    message: (value) => value.trim().length >= 10,
  };

  const errorMessages = {
    name: "Vul je volledige naam in (minimaal 2 tekens).",
    email: "Vul een geldig e-mailadres in.",
    message: "Je bericht moet minimaal 10 tekens bevatten.",
  };

  function setFieldError(fieldName, message) {
    const field = form.querySelector(`[name="${fieldName}"]`);
    if (!field) return;
    const wrapper = field.closest(".field");
    const errorEl = wrapper ? wrapper.querySelector(".error-msg") : null;
    if (message) {
      wrapper && wrapper.classList.add("has-error");
      if (errorEl) errorEl.textContent = message;
      field.setAttribute("aria-invalid", "true");
    } else {
      wrapper && wrapper.classList.remove("has-error");
      if (errorEl) errorEl.textContent = "";
      field.removeAttribute("aria-invalid");
    }
  }

  function validate() {
    let isValid = true;
    Object.keys(validators).forEach((fieldName) => {
      const field = form.querySelector(`[name="${fieldName}"]`);
      if (!field) return;
      const ok = validators[fieldName](field.value);
      setFieldError(fieldName, ok ? "" : errorMessages[fieldName]);
      if (!ok) isValid = false;
    });
    return isValid;
  }

  // Live-validate on blur for immediate, non-intrusive feedback.
  Object.keys(validators).forEach((fieldName) => {
    const field = form.querySelector(`[name="${fieldName}"]`);
    if (!field) return;
    field.addEventListener("blur", () => {
      const ok = validators[fieldName](field.value);
      setFieldError(fieldName, ok ? "" : errorMessages[fieldName]);
    });
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    // Honeypot: a hidden field that only bots tend to fill in.
    const honeypot = form.querySelector('[name="website"]');
    if (honeypot && honeypot.value.trim() !== "") {
      // Silently drop likely-bot submissions without revealing detection.
      form.reset();
      return;
    }

    if (!validate()) {
      if (status) {
        status.textContent = "Controleer de gemarkeerde velden en probeer het opnieuw.";
        status.className = "form-status is-error";
      }
      const firstError = form.querySelector(".has-error input, .has-error textarea");
      if (firstError) firstError.focus();
      return;
    }

    // No backend is connected in this static demo. In production this
    // request should POST to a server that re-validates all input,
    // enforces CSRF protection, and rate-limits submissions.
    if (status) {
      status.textContent =
        "Bedankt voor je bericht! We nemen zo spoedig mogelijk contact met je op.";
      status.className = "form-status is-success";
    }
    form.reset();
  });
}

/* ---------------------------------------------------------------------- */
/* Header shadow on scroll                                                 */
/* ---------------------------------------------------------------------- */
function initHeaderShadowOnScroll() {
  const header = document.querySelector(".site-header");
  if (!header) return;

  const update = () => {
    if (window.scrollY > 8) {
      header.style.boxShadow = "0 4px 20px rgba(6, 35, 29, 0.08)";
    } else {
      header.style.boxShadow = "none";
    }
  };

  update();
  window.addEventListener("scroll", update, { passive: true });
}
