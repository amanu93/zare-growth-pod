// Booking link for every "Book a call" button. Change it here; the href in index.html
// is only a fallback for visitors without JavaScript.
const BOOKING_URL = "https://calendly.com/emanuel-ypgh/30min";

document.querySelectorAll("[data-booking]").forEach((link) => {
  link.href = BOOKING_URL;
});

// Fade sections in as they scroll into view. Only sections that start below the
// fold are hidden, so nothing visible on load is delayed.
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!reduceMotion && "IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -10% 0px" }
  );

  document.querySelectorAll("main > section, .site-footer").forEach((section) => {
    if (section.getBoundingClientRect().top > window.innerHeight) {
      section.classList.add("reveal");
      observer.observe(section);
    }
  });
}
