/* ============================================
   LIFELINE DASHBOARD - JAVASCRIPT
   Interactive dashboard with animations
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {

  /* ============================================
     ANIMATED COUNTER
     Count up animation for stat values
     ============================================ */
  function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16); // 60fps
    let current = start;

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

  // Trigger counter animation when stat cards are visible
  const statValues = document.querySelectorAll('.stat-value[data-count]');
  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px'
  };

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
        const target = parseInt(entry.target.getAttribute('data-count'));
        animateCounter(entry.target, target);
        entry.target.classList.add('counted');
      }
    });
  }, observerOptions);

  statValues.forEach(stat => counterObserver.observe(stat));

  /* ============================================
     PROGRESS BAR ANIMATION
     Animate progress bars when visible
     ============================================ */
  const progressBars = document.querySelectorAll('.progress[data-progress]');
  
  const progressObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const progress = entry.target.getAttribute('data-progress');
        entry.target.style.width = progress + '%';
      }
    });
  }, observerOptions);

  progressBars.forEach(bar => progressObserver.observe(bar));

  /* ============================================
     STAT CARD INTERACTIONS
     Add interactive effects to stat cards
     ============================================ */
  const statCards = document.querySelectorAll('.stat-card');
  
  statCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      // Add ripple effect
      const ripple = document.createElement('div');
      ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(22, 163, 74, 0.2);
        width: 100px;
        height: 100px;
        pointer-events: none;
        animation: ripple 0.6s ease-out;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
      `;
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });

  // Add ripple animation keyframes
  const style = document.createElement('style');
  style.textContent = `
    @keyframes ripple {
      from {
        transform: translate(-50%, -50%) scale(0);
        opacity: 1;
      }
      to {
        transform: translate(-50%, -50%) scale(2);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

  /* ============================================
     GOAL ITEM INTERACTIONS
     Enhance goal items with hover effects
     ============================================ */
  const goalItems = document.querySelectorAll('.goal-item');
  
  goalItems.forEach(item => {
    item.addEventListener('click', function() {
      // Add pulse animation
      this.style.animation = 'pulse 0.5s ease-out';
      setTimeout(() => {
        this.style.animation = '';
      }, 500);
    });
  });

  /* ============================================
     ACHIEVEMENT ANIMATIONS
     Celebrate achievements with effects
     ============================================ */
  const achievementItems = document.querySelectorAll('.achievement-item');
  
  achievementItems.forEach((item, index) => {
    // Stagger animation
    item.style.animationDelay = `${index * 0.1}s`;
    
    item.addEventListener('mouseenter', function() {
      const icon = this.querySelector('.trophy-icon');
      if (icon) {
        icon.style.transform = 'scale(1.2) rotate(10deg)';
        icon.style.transition = 'transform 0.3s ease';
      }
    });
    
    item.addEventListener('mouseleave', function() {
      const icon = this.querySelector('.trophy-icon');
      if (icon) {
        icon.style.transform = 'scale(1) rotate(0deg)';
      }
    });
  });

  /* ============================================
     CHART BAR INTERACTIONS
     Interactive weekly progress chart
     ============================================ */
  const chartBars = document.querySelectorAll('.chart-bar');
  
  chartBars.forEach(bar => {
    bar.addEventListener('click', function() {
      // Remove active class from all bars
      chartBars.forEach(b => b.classList.remove('active'));
      // Add active class to clicked bar
      this.classList.add('active');
    });
  });

  /* ============================================
     QUICK ACTION BUTTONS
     Add feedback to quick action buttons
     ============================================ */
  const quickActionBtns = document.querySelectorAll('.quick-action-btn');
  
  quickActionBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      // Create success ripple
      const rect = this.getBoundingClientRect();
      const ripple = document.createElement('div');
      ripple.style.cssText = `
        position: fixed;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        width: 20px;
        height: 20px;
        pointer-events: none;
        animation: quickRipple 0.6s ease-out;
        left: ${e.clientX - 10}px;
        top: ${e.clientY - 10}px;
        z-index: 9999;
      `;
      document.body.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });

  const quickRippleStyle = document.createElement('style');
  quickRippleStyle.textContent = `
    @keyframes quickRipple {
      from {
        transform: scale(1);
        opacity: 1;
      }
      to {
        transform: scale(3);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(quickRippleStyle);

  /* ============================================
     VIEW ALL LINKS
     Smooth scroll or navigation
     ============================================ */
  const viewAllLinks = document.querySelectorAll('.view-all-link');
  
  viewAllLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Add loading animation if navigating
      if (this.tagName === 'A' && this.getAttribute('href')) {
        this.style.opacity = '0.6';
        this.textContent = 'Loading...';
      }
    });
  });

  /* ============================================
     EMPTY STATE BUTTON
     Animate empty state actions
     ============================================ */
  const emptyStateBtns = document.querySelectorAll('.empty-state-btn');
  
  emptyStateBtns.forEach(btn => {
    btn.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-2px) scale(1.05)';
    });
    
    btn.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });

  /* ============================================
     WELCOME CARD GREETING
     Dynamic greeting based on time of day
     ============================================ */
  function updateGreeting() {
    const hour = new Date().getHours();
    const welcomeHeading = document.querySelector('.welcome-card h2');
    
    if (welcomeHeading) {
      let greeting = 'Welcome back';
      let emoji = '👋';
      
      if (hour < 12) {
        greeting = 'Good morning';
        emoji = '🌅';
      } else if (hour < 18) {
        greeting = 'Good afternoon';
        emoji = '☀️';
      } else {
        greeting = 'Good evening';
        emoji = '🌙';
      }
      
      const username = welcomeHeading.textContent.split(',')[1] || '!';
      welcomeHeading.textContent = `${greeting},${username} ${emoji}`;
    }
  }

  updateGreeting();

  /* ============================================
     REFRESH DATA
     Auto-refresh dashboard data
     ============================================ */
  function refreshDashboard() {
    // Add shimmer effect to indicate loading
    const cards = document.querySelectorAll('.card, .stat-card');
    cards.forEach(card => {
      card.style.opacity = '0.7';
    });
    
    // Simulate data refresh (replace with actual API call)
    setTimeout(() => {
      cards.forEach(card => {
        card.style.opacity = '1';
        card.style.transition = 'opacity 0.3s ease';
      });
      console.log('Dashboard refreshed');
    }, 500);
  }

  // Optional: Auto-refresh every 5 minutes
  // setInterval(refreshDashboard, 300000);

  /* ============================================
     KEYBOARD SHORTCUTS
     Add keyboard navigation
     ============================================ */
  document.addEventListener('keydown', function(e) {
    // Press 'r' to refresh dashboard
    if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
      const activeElement = document.activeElement;
      if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
        refreshDashboard();
      }
    }
    
    // Press 'g' to navigate to goals
    if (e.key === 'g' && !e.ctrlKey && !e.metaKey) {
      const goalsLink = document.querySelector('a[href*="goals"]');
      if (goalsLink) goalsLink.click();
    }
  });

  /* ============================================
     PARALLAX EFFECT
     Subtle parallax on scroll
     ============================================ */
  window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const orbs = document.querySelectorAll('.gradient-orb');
    
    orbs.forEach((orb, index) => {
      const speed = 0.1 + (index * 0.05);
      orb.style.transform = `translateY(${scrolled * speed}px)`;
    });
  });

  /* ============================================
     PERFORMANCE MONITORING
     Log dashboard load time
     ============================================ */
  window.addEventListener('load', function() {
    if (window.performance && window.performance.timing) {
      const loadTime = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;
      console.log(`📊 Dashboard loaded in ${loadTime}ms`);
    }
  });

  /* ============================================
     CONSOLE WELCOME MESSAGE
     Fun message for developers
     ============================================ */
  console.log(
    '%c📊 LifeLine Dashboard',
    'background: linear-gradient(135deg, #16a34a, #22c55e); color: white; padding: 10px 20px; font-size: 18px; font-weight: bold; border-radius: 8px;'
  );
  console.log(
    '%cDashboard loaded successfully! 🚀',
    'color: #16a34a; font-size: 14px; font-weight: 500;'
  );
  console.log(
    '%cKeyboard shortcuts: Press "r" to refresh, "g" for goals',
    'color: #6b7280; font-size: 12px;'
  );

});

/* ============================================
   UTILITY FUNCTIONS
   Reusable helper functions
   ============================================ */

// Format numbers with commas
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Calculate completion percentage
function calculateProgress(completed, total) {
  if (total === 0) return 0;
  return Math.round((completed / total) * 100);
}

// Generate random color for charts
function getRandomColor() {
  const colors = ['#16a34a', '#22c55e', '#3b82f6', '#f59e0b', '#ef4444'];
  return colors[Math.floor(Math.random() * colors.length)];
}

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