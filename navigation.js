// Navigation Menu JavaScript - Updated
document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu toggle
  const mobileMenuToggle = document.getElementById("mobile-menu-toggle");
  const navList = document.getElementById("nav-list");

  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener("click", function () {
      navList.classList.toggle("show");
    });
  }

  // Mobile dropdown toggle
  const navDropdowns = document.querySelectorAll(".nav-dropdown");

  navDropdowns.forEach((dropdown) => {
    const link = dropdown.querySelector(".nav-link");

    // For mobile only
    if (link) {
      link.addEventListener("click", function (e) {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          dropdown.classList.toggle("show");
        }
      });
    }
  });

  // Close mobile menu when clicking on a non-dropdown item
  const navLinks = document.querySelectorAll(
    ".nav-item:not(.nav-dropdown) .nav-link, .dropdown-item"
  );
  navLinks.forEach((link) => {
    link.addEventListener("click", function () {
      if (window.innerWidth <= 768) {
        navList.classList.remove("show");
      }
    });
  });

  // Mark active menu item based on current URL
  function setActiveMenuItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach((link) => {
      const href = link.getAttribute("href");
      const parentLi = link.parentElement;

      if (
        href === currentPath ||
        (href !== "/" && currentPath.startsWith(href))
      ) {
        parentLi.classList.add("active");
      } else {
        parentLi.classList.remove("active");
      }
    });
  }

  setActiveMenuItem();
});
