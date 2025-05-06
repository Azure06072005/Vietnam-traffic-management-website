// Navigation Menu JavaScript - Updated for Dash
document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu toggle
  const mobileMenuToggle = document.getElementById("mobile-menu-toggle");
  const navList = document.getElementById("nav-list");
  const navRight = document.getElementById("nav-right");

  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener("click", function () {
      navList.classList.toggle("show");
      if (navRight) {
        navRight.classList.toggle("show");
      }
    });
  }

  // Mobile dropdown toggle
  const navDropdowns = document.querySelectorAll(".nav-dropdown");

  navDropdowns.forEach((dropdown) => {
    const link = dropdown.querySelector(".nav-link");

    // For mobile only
    if (link) {
      link.addEventListener("click", function (e) {
        if (window.innerWidth <= 992) {
          e.preventDefault();
          dropdown.classList.toggle("show");
        }
      });
    }
  });

  // Language selector functionality
  const languageSelector = document.getElementById("language-selector");
  if (languageSelector) {
    languageSelector.addEventListener("click", function (e) {
      if (window.innerWidth <= 992) {
        e.preventDefault();
        const languageDropdown = document.getElementById("language-dropdown");
        if (languageDropdown) {
          languageDropdown.classList.toggle("show");
        }
      }
    });
  }

  // User profile dropdown
  const userProfile = document.getElementById("user-profile");
  if (userProfile) {
    userProfile.addEventListener("click", function (e) {
      if (window.innerWidth <= 992) {
        e.preventDefault();
        const userDropdown = document.getElementById("user-dropdown");
        if (userDropdown) {
          userDropdown.classList.toggle("show");
        }
      }
    });
  }

  // Close mobile menu when clicking on a non-dropdown item
  const navLinks = document.querySelectorAll(
    ".nav-item:not(.nav-dropdown) .nav-link, .dropdown-item"
  );
  navLinks.forEach((link) => {
    link.addEventListener("click", function () {
      if (window.innerWidth <= 992) {
        navList.classList.remove("show");
        if (navRight) {
          navRight.classList.remove("show");
        }
      }
    });
  });

  // Close dropdowns when clicking outside
  document.addEventListener("click", function (e) {
    // Don't close if clicked inside a dropdown
    if (
      e.target.closest(".nav-dropdown") ||
      e.target.closest(".language-selector") ||
      e.target.closest(".user-profile")
    ) {
      return;
    }

    // Close all open dropdowns
    const openDropdowns = document.querySelectorAll(".dropdown-menu.show");
    openDropdowns.forEach((dropdown) => {
      dropdown.classList.remove("show");
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
