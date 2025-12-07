/* ============================================
   PROFILE.JS - JavaScript Interactions
   Profile page functionality for LifeLine
   ============================================ */

// ============================================
// EDIT MODE TOGGLE - START
// Switch between view and edit modes
// ============================================
document.addEventListener('DOMContentLoaded', function() {
  const editBtn = document.getElementById("editBtn");
  const cancelBtn = document.getElementById("cancelBtn");
  const viewMode = document.getElementById("viewMode");
  const editMode = document.getElementById("editMode");

  if (editBtn && cancelBtn && viewMode && editMode) {
    // Switch to edit mode
    editBtn.addEventListener("click", () => {
      viewMode.style.display = "none";
      editMode.style.display = "block";
      editBtn.style.display = "none";
      
      // Add animation
      editMode.style.animation = "fadeIn 0.4s ease-out";
      
      // Focus first input
      const firstInput = editMode.querySelector('input');
      if (firstInput) {
        setTimeout(() => firstInput.focus(), 100);
      }
    });

    // Switch to view mode
    cancelBtn.addEventListener("click", () => {
      // Confirm if user wants to discard changes
      const inputs = editMode.querySelectorAll('input, textarea');
      let hasChanges = false;
      
      inputs.forEach(input => {
        if (input.defaultValue !== input.value) {
          hasChanges = true;
        }
      });
      
      if (hasChanges) {
        if (!confirm('You have unsaved changes. Are you sure you want to cancel?')) {
          return;
        }
      }
      
      viewMode.style.display = "block";
      editMode.style.display = "none";
      editBtn.style.display = "inline-flex";
      
      // Reset form to original values
      inputs.forEach(input => {
        input.value = input.defaultValue;
      });
    });
  }
});
// EDIT MODE TOGGLE - END

// ============================================
// FORM VALIDATION - START
// Real-time form validation with visual feedback
// ============================================
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('editMode');
  
  if (form) {
    const inputs = form.querySelectorAll('input, textarea');
    
    inputs.forEach(input => {
      // Validate on input
      input.addEventListener('input', function() {
        validateField(this);
      });
      
      // Validate on blur
      input.addEventListener('blur', function() {
        validateField(this);
      });
    });
    
    // Form submission validation
    form.addEventListener('submit', function(e) {
      let isValid = true;
      
      inputs.forEach(input => {
        if (!validateField(input)) {
          isValid = false;
        }
      });
      
      if (!isValid) {
        e.preventDefault();
        showNotification('error', 'Please fix the errors before submitting.');
      }
    });
  }
});

function validateField(field) {
  const value = field.value.trim();
  const fieldName = field.name;
  let isValid = true;
  let errorMessage = '';
  
  // Required field validation
  if (field.hasAttribute('required') && value === '') {
    isValid = false;
    errorMessage = 'This field is required';
  }
  
  // Email validation
  if (fieldName === 'email' && value !== '') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      isValid = false;
      errorMessage = 'Please enter a valid email';
    }
  }
  
  // Username validation (min 3 characters)
  if (fieldName === 'username' && value.length > 0 && value.length < 3) {
    isValid = false;
    errorMessage = 'Username must be at least 3 characters';
  }
  
  // Update field styling
  if (!isValid) {
    field.style.borderColor = '#ef4444';
    field.style.boxShadow = '0 0 0 4px rgba(239, 68, 68, 0.1)';
    
    // Show error message
    let errorDiv = field.parentElement.querySelector('.error-message');
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      field.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = errorMessage;
    errorDiv.style.color = '#ef4444';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
  } else {
    field.style.borderColor = '#27ae60';
    field.style.boxShadow = '0 0 0 4px rgba(39, 174, 96, 0.1)';
    
    // Remove error message
    const errorDiv = field.parentElement.querySelector('.error-message');
    if (errorDiv) {
      errorDiv.remove();
    }
  }
  
  return isValid;
}
// FORM VALIDATION - END

// ============================================
// NOTIFICATION SYSTEM - START
// Show toast notifications
// ============================================
function showNotification(type, message) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  
  // Styling
  Object.assign(notification.style, {
    position: 'fixed',
    top: '20px',
    right: '20px',
    padding: '1rem 1.5rem',
    borderRadius: '10px',
    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
    zIndex: '9999',
    maxWidth: '400px',
    animation: 'slideInRight 0.4s ease-out',
    fontWeight: '500'
  });
  
  // Color based on type
  if (type === 'success') {
    notification.style.background = '#f0fdf4';
    notification.style.color = '#166534';
    notification.style.border = '1px solid #bbf7d0';
  } else if (type === 'error') {
    notification.style.background = '#fef2f2';
    notification.style.color = '#991b1b';
    notification.style.border = '1px solid #fecaca';
  } else if (type === 'info') {
    notification.style.background = '#eff6ff';
    notification.style.color = '#1e40af';
    notification.style.border = '1px solid #bfdbfe';
  }
  
  // Add to page
  document.body.appendChild(notification);
  
  // Auto remove after 5 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOutRight 0.4s ease-out';
    setTimeout(() => {
      notification.remove();
    }, 400);
  }, 5000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  @keyframes slideOutRight {
    from {
      opacity: 1;
      transform: translateX(0);
    }
    to {
      opacity: 0;
      transform: translateX(100px);
    }
  }
`;
document.head.appendChild(style);
// NOTIFICATION SYSTEM - END

// ============================================
// AUTO-HIDE MESSAGES - START
// Automatically hide Django messages after delay
// ============================================
document.addEventListener('DOMContentLoaded', function() {
  const alerts = document.querySelectorAll('.alert');
  
  alerts.forEach(alert => {
    // Auto-hide after 5 seconds
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      
      setTimeout(() => {
        alert.remove();
      }, 500);
    }, 5000);
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✖';
    closeBtn.style.cssText = `
      margin-left: auto;
      background: none;
      border: none;
      font-size: 1.2rem;
      cursor: pointer;
      padding: 0;
      opacity: 0.6;
      transition: opacity 0.2s;
    `;
    closeBtn.addEventListener('mouseover', () => closeBtn.style.opacity = '1');
    closeBtn.addEventListener('mouseout', () => closeBtn.style.opacity = '0.6');
    closeBtn.addEventListener('click', () => {
      alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 300);
    });
    
    alert.appendChild(closeBtn);
  });
});
// AUTO-HIDE MESSAGES - END

// ============================================
// CHARACTER COUNTER - START
// Show character count for bio textarea
// ============================================
document.addEventListener('DOMContentLoaded', function() {
  const bioTextarea = document.querySelector('textarea[name="bio"]');
  
  if (bioTextarea) {
    const maxLength = 500;
    
    // Create counter element
    const counter = document.createElement('div');
    counter.className = 'character-counter';
    counter.style.cssText = `
      text-align: right;
      font-size: 0.875rem;
      color: #6b7280;
      margin-top: 0.5rem;
    `;
    
    bioTextarea.parentElement.appendChild(counter);
    
    // Update counter
    function updateCounter() {
      const remaining = maxLength - bioTextarea.value.length;
      counter.textContent = `${bioTextarea.value.length} / ${maxLength} characters`;
      
      if (remaining < 50) {
        counter.style.color = '#ef4444';
      } else if (remaining < 100) {
        counter.style.color = '#f59e0b';
      } else {
        counter.style.color = '#6b7280';
      }
    }
    
    bioTextarea.addEventListener('input', updateCounter);
    updateCounter(); // Initial count
  }
});
// CHARACTER COUNTER - END

// ============================================
// KEYBOARD SHORTCUTS - START
// Useful keyboard shortcuts for profile page
// ============================================
document.addEventListener('keydown', function(e) {
  // Press 'E' to toggle edit mode (when not in input)
  if (e.key === 'e' && !e.target.matches('input, textarea')) {
    const editBtn = document.getElementById('editBtn');
    if (editBtn && editBtn.style.display !== 'none') {
      editBtn.click();
    }
  }
  
  // Press 'Escape' to cancel edit mode
  if (e.key === 'Escape') {
    const cancelBtn = document.getElementById('cancelBtn');
    const editMode = document.getElementById('editMode');
    if (cancelBtn && editMode && editMode.style.display !== 'none') {
      cancelBtn.click();
    }
  }
  
  // Press 'Ctrl+S' or 'Cmd+S' to save (in edit mode)
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    const editMode = document.getElementById('editMode');
    if (editMode && editMode.style.display !== 'none') {
      e.preventDefault();
      editMode.submit();
    }
  }
});
// KEYBOARD SHORTCUTS - END

// ============================================
// CARD ANIMATIONS - START
// Animate cards on scroll
// ============================================
document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.card');
  
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);
  
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
    observer.observe(card);
  });
});
// CARD ANIMATIONS - END

// ============================================
// STATS ANIMATION - START
// Animate stat numbers on load
// ============================================
document.addEventListener('DOMContentLoaded', function() {
  const statValues = document.querySelectorAll('.stat-value');
  
  statValues.forEach(stat => {
    const finalValue = parseInt(stat.textContent);
    if (!isNaN(finalValue)) {
      let currentValue = 0;
      const increment = finalValue / 50; // 50 steps
      
      const timer = setInterval(() => {
        currentValue += increment;
        if (currentValue >= finalValue) {
          stat.textContent = finalValue;
          clearInterval(timer);
        } else {
          stat.textContent = Math.floor(currentValue);
        }
      }, 20);
    }
  });
});
// STATS ANIMATION - END

// ============================================
// CONSOLE BRANDING - START
// Fun message for developers
// ============================================
console.log('%c🌱 LifeLine Profile Page', 'color: #27ae60; font-size: 20px; font-weight: bold;');
console.log('%cManage your personal growth journey', 'color: #6b7280; font-size: 14px;');
console.log('%c© 2025 LifeLine', 'color: #a7f3d0; font-size: 12px;');
console.log('%cKeyboard shortcuts: E (edit), ESC (cancel), Ctrl+S (save)', 'color: #27ae60; font-size: 12px; font-style: italic;');
// CONSOLE BRANDING - END