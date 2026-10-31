/**
 * Navigation & Theme Controller
 * Ashish's Portfolio
 */
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
  });

  /* --------------------------------------------------------------------------
     1. THEME CONTROLLER
     -------------------------------------------------------------------------- */
  function initTheme() {
    var themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    function getActiveTheme() {
      return document.documentElement.getAttribute('data-theme') || 'dark';
    }

    function applyTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      var isDark = theme === 'dark';
      themeToggle.setAttribute('aria-pressed', isDark ? 'false' : 'true');
      themeToggle.setAttribute('aria-label', isDark ? 'Switch to light theme' : 'Switch to dark theme');
      themeToggle.setAttribute('title', isDark ? 'Switch to light theme' : 'Switch to dark theme');
    }

    // Set initial button state based on active theme
    applyTheme(getActiveTheme());

    // Toggle theme on button click
    themeToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      var current = getActiveTheme();
      var next = current === 'dark' ? 'light' : 'dark';
      localStorage.setItem('portfolio-theme', next);
      applyTheme(next);
    });

    // Listen to system changes if user hasn't explicitly set a preference
    try {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('portfolio-theme')) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    } catch (err) {
      // Legacy browsers
    }
  }

  /* --------------------------------------------------------------------------
     2. ACCESSIBLE MOBILE NAVIGATION CONTROLLER
     -------------------------------------------------------------------------- */
  function initNavigation() {
    var toggleBtn = document.getElementById('nav-toggle');
    var navMenu = document.getElementById('primary-nav');

    if (!toggleBtn || !navMenu) return;

    var navLinks = navMenu.querySelectorAll('a');

    function openMenu() {
      navMenu.classList.add('is-open');
      toggleBtn.classList.add('is-active');
      toggleBtn.setAttribute('aria-expanded', 'true');
      toggleBtn.setAttribute('aria-label', 'Close navigation menu');
    }

    function closeMenu(returnFocus) {
      if (!navMenu.classList.contains('is-open')) return;
      navMenu.classList.remove('is-open');
      toggleBtn.classList.remove('is-active');
      toggleBtn.setAttribute('aria-expanded', 'false');
      toggleBtn.setAttribute('aria-label', 'Open navigation menu');
      if (returnFocus && typeof toggleBtn.focus === 'function') {
        toggleBtn.focus();
      }
    }

    // Toggle button click handler
    toggleBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      var isOpen = navMenu.classList.contains('is-open');
      if (isOpen) {
        closeMenu(false);
      } else {
        openMenu();
      }
    });

    // Close menu when clicking on any navigation link
    navLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        closeMenu(false);
      });
    });

    // Close menu when pressing Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' || e.key === 'Esc') {
        closeMenu(true);
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (navMenu.classList.contains('is-open')) {
        if (!navMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
          closeMenu(false);
        }
      }
    });

    // Handle viewport resize: reset mobile state if resized to desktop
    window.addEventListener('resize', function() {
      if (window.innerWidth >= 768 && navMenu.classList.contains('is-open')) {
        closeMenu(false);
      }
    });
  }
})();
