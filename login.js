// Login JavaScript Enhancements
document.addEventListener("DOMContentLoaded", function () {
  // Auto-focus vào username input khi trang load
  const usernameInput = document.getElementById("username-input");
  if (usernameInput) {
    usernameInput.focus();
  }

  // Xử lý Enter key để submit form
  const loginInputs = document.querySelectorAll(".login-input");
  const loginButton = document.getElementById("login-button");

  loginInputs.forEach((input) => {
    input.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        if (loginButton) {
          loginButton.click();
        }
      }
    });
  });

  // Thêm loading animation cho nút đăng nhập
  if (loginButton) {
    loginButton.addEventListener("click", function () {
      this.classList.add("loading");
      this.disabled = true;

      // Remove loading state after 3 seconds (as fallback)
      setTimeout(() => {
        this.classList.remove("loading");
        this.disabled = false;
      }, 3000);
    });
  }

  // Toggle password visibility (Optional enhancement)
  const passwordInput = document.getElementById("password-input");
  if (passwordInput) {
    const toggleButton = document.createElement("button");
    toggleButton.type = "button";
    toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
    toggleButton.className = "password-toggle";
    toggleButton.onclick = function () {
      const type =
        passwordInput.getAttribute("type") === "password" ? "text" : "password";
      passwordInput.setAttribute("type", type);
      this.innerHTML =
        type === "password"
          ? '<i class="fas fa-eye"></i>'
          : '<i class="fas fa-eye-slash"></i>';
    };

    // Insert toggle button after password input
    passwordInput.parentNode.insertBefore(
      toggleButton,
      passwordInput.nextSibling
    );
  }

  // Auto-clear error messages when user starts typing
  const errorDiv = document.getElementById("login-error");
  if (errorDiv) {
    loginInputs.forEach((input) => {
      input.addEventListener("input", function () {
        if (errorDiv.classList.contains("show")) {
          errorDiv.classList.remove("show");
        }
      });
    });
  }

  // Simple form validation
  function validateForm() {
    const username = document.getElementById("username-input").value;
    const password = document.getElementById("password-input").value;

    let isValid = true;
    let errorMessage = "";

    if (!username.trim()) {
      errorMessage = "Vui lòng nhập tên đăng nhập";
      isValid = false;
    } else if (!password.trim()) {
      errorMessage = "Vui lòng nhập mật khẩu";
      isValid = false;
    }

    if (!isValid && errorDiv) {
      errorDiv.textContent = errorMessage;
      errorDiv.classList.add("show");
    }

    return isValid;
  }

  // Enhanced button click handler
  if (loginButton) {
    const originalClickHandler = loginButton.onclick;
    loginButton.onclick = function (e) {
      if (!validateForm()) {
        e.preventDefault();
        return false;
      }

      this.classList.add("loading");
      this.disabled = true;

      // Call original handler if exists
      if (originalClickHandler) {
        originalClickHandler.call(this, e);
      }
    };
  }

  // Smooth error message animation
  const style = document.createElement("style");
  style.textContent = `
        .password-toggle {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #666;
            cursor: pointer;
            padding: 5px;
            font-size: 14px;
        }
        
        .password-toggle:hover {
            color: #333;
        }
        
        .login-field {
            position: relative;
        }
        
        .login-input:focus + .password-toggle,
        .password-toggle:focus {
            outline: none;
        }
        
        .remember-checkbox input[type="checkbox"] {
            margin-right: 8px;
            transform: scale(1.1);
        }
        
        .login-demo-section {
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .login-demo-section:hover {
            background-color: #e8f4ff;
            transform: scale(1.02);
        }
    `;
  document.head.appendChild(style);

  // Quick-fill demo credentials on demo section click
  const demoSection = document.querySelector(".login-demo-section");
  if (demoSection) {
    demoSection.addEventListener("click", function () {
      const usernameInput = document.getElementById("username-input");
      const passwordInput = document.getElementById("password-input");

      if (usernameInput && passwordInput) {
        usernameInput.value = "admin";
        passwordInput.value = "123456";

        // Trigger input events to update Dash
        usernameInput.dispatchEvent(new Event("input", { bubbles: true }));
        passwordInput.dispatchEvent(new Event("input", { bubbles: true }));

        // Add a visual feedback
        this.style.background = "#d4edda";
        setTimeout(() => {
          this.style.background = "";
        }, 500);
      }
    });
  }

  // Add keyboard navigation for demo section
  if (demoSection) {
    demoSection.setAttribute("tabindex", "0");
    demoSection.addEventListener("keypress", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.click();
      }
    });
  }

  // Initialize tooltips for enhanced UX (if Bootstrap is available)
  if (typeof bootstrap !== "undefined") {
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
});

// Session management
function checkSession() {
  // This function can be enhanced to check session validity
  // For now, it's a placeholder for future enhancements
  return true;
}

// Auto-logout functionality (optional)
function setupAutoLogout(timeoutMinutes = 30) {
  let timeoutId;

  function resetTimer() {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      if (confirm("Phiên đăng nhập đã hết hạn. Bạn có muốn tiếp tục?")) {
        resetTimer();
      } else {
        window.location.href = "/logout";
      }
    }, timeoutMinutes * 60 * 1000);
  }

  // Reset timer on user activity
  ["mousedown", "mousemove", "keypress", "scroll", "touchstart"].forEach(
    (event) => {
      document.addEventListener(event, resetTimer, true);
    }
  );

  // Initial timer
  resetTimer();
}

// Call auto-logout function (uncomment if needed)
// setupAutoLogout(30); // 30 minutes
