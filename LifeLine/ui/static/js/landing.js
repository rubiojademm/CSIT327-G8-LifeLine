/* ============================================
   LIFELINE LANDING PAGE - JAVASCRIPT
   Interactive enhancements and animations
   ============================================ */

// Wait for DOM to be fully loaded before running scripts
document.addEventListener('DOMContentLoaded', function() {
  
  /* ============================================
     SMOOTH SCROLLING
     Enable smooth scroll for anchor links
     ============================================ */
  const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
  
  smoothScrollLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      
      // Only smooth scroll if it's an internal anchor
      if (href !== '#' && href.startsWith('#')) {
        e.preventDefault();
        const target = document.querySelector(href);
        
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  /* ============================================
     INTERSECTION OBSERVER
     Animate elements when they enter viewport
     ============================================ */
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, observerOptions);

  // Observe all feature cards
  const features = document.querySelectorAll('.feature');
  features.forEach(feature => {
    observer.observe(feature);
  });

  /* ============================================
     PARALLAX EFFECT FOR PARTICLES
     Add subtle mouse-following effect to particles
     ============================================ */
  const particles = document.querySelectorAll('.particle');
  
  document.addEventListener('mousemove', function(e) {
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    particles.forEach((particle, index) => {
      // Different speed for each particle
      const speed = (index + 1) * 10;
      const x = (mouseX - 0.5) * speed;
      const y = (mouseY - 0.5) * speed;
      
      particle.style.transform = `translate(${x}px, ${y}px)`;
    });
  });

  /* ============================================
     BUTTON CLICK RIPPLE EFFECT
     Enhanced visual feedback on button clicks
     ============================================ */
  const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
  
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      // Create ripple element
      const ripple = document.createElement('span');
      ripple.classList.add('ripple-effect');
      
      // Position ripple at click location
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      
      this.appendChild(ripple);
      
      // Remove ripple after animation
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });

  /* ============================================
     FEATURE CARD TILT EFFECT
     3D tilt effect on mouse move over cards
     ============================================ */
  features.forEach(feature => {
    feature.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = (y - centerY) / 10;
      const rotateY = (centerX - x) / 10;
      
      this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
    });
    
    feature.addEventListener('mouseleave', function() {
      this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
    });
  });

  /* ============================================
     ANIMATED COUNTER
     Count up numbers if they exist on the page
     ============================================ */
  function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16); // 60fps
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = Math.round(target);
        clearInterval(timer);
      } else {
        element.textContent = Math.round(current);
      }
    }, 16);
  }

  // Example usage if you add counter elements later
  const counters = document.querySelectorAll('[data-count]');
  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-count'));
    observer.observe(counter);
    
    counter.addEventListener('in-view', () => {
      animateCounter(counter, target);
    });
  });

  /* ============================================
     LAZY LOADING IMAGES
     Load images only when they're about to enter viewport
     ============================================ */
  const lazyImages = document.querySelectorAll('img[data-src]');
  
  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.getAttribute('data-src');
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });
  
  lazyImages.forEach(img => imageObserver.observe(img));

  /* ============================================
     SCROLL PROGRESS INDICATOR
     Show reading progress at top of page
     ============================================ */
  function updateScrollProgress() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;
    
    // You can add a progress bar element and update it here
    // Example: document.querySelector('.progress-bar').style.width = progress + '%';
  }
  
  window.addEventListener('scroll', updateScrollProgress);

  /* ============================================
     MOBILE MENU TOGGLE
     Handle mobile navigation if needed in future
     ============================================ */
  const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');
  
  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener('click', function() {
      mobileMenu.classList.toggle('active');
      this.classList.toggle('active');
    });
  }

  /* ============================================
     FORM VALIDATION
     Client-side validation for future forms
     ============================================ */
  const forms = document.querySelectorAll('form[data-validate]');
  
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      let isValid = true;
      const inputs = this.querySelectorAll('input[required], textarea[required]');
      
      inputs.forEach(input => {
        if (!input.value.trim()) {
          isValid = false;
          input.classList.add('error');
        } else {
          input.classList.remove('error');
        }
      });
      
      if (isValid) {
        this.submit();
      }
    });
  });

  /* ============================================
     CONSOLE EASTER EGG
     Fun message for developers
     ============================================ */
  console.log('%c🎯 LifeLine ', 'background: linear-gradient(90deg, #27ae60, #2ecc71); color: white; padding: 10px 20px; font-size: 20px; font-weight: bold;');
  console.log('%cLooking at the code? We like your style! 🚀', 'color: #27ae60; font-size: 14px;');
  console.log('%cCheck out our careers page if you want to build cool stuff with us!', 'color: #6b7280; font-size: 12px;');

  /* ============================================
     PERFORMANCE MONITORING
     Log page load time for optimization
     ============================================ */
  window.addEventListener('load', function() {
    const loadTime = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;
    console.log(`⚡ Page loaded in ${loadTime}ms`);
  });

});

/* ============================================
   UTILITY FUNCTIONS
   Reusable helper functions
   ============================================ */

// Debounce function for performance
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Throttle function for scroll events
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Check if element is in viewport
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}