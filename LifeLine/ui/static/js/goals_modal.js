/* ============================================
   GOAL MODALS - JAVASCRIPT
   Handles both Create Goal and Update Progress modals
   ============================================ */

/* ============================================
   CREATE GOAL MODAL FUNCTIONS
   ============================================ */

/**
 * Open the Create Goal modal
 */
function openCreateGoalModal() {
  const modal = document.getElementById("createGoalModal");
  if (modal) {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden"; // Prevent background scrolling
    
    // Focus on first input field
    setTimeout(() => {
      const firstInput = modal.querySelector('input[type="text"]');
      if (firstInput) firstInput.focus();
    }, 100);
  }
}

/**
 * Close the Create Goal modal
 */
function closeCreateGoalModal() {
  const modal = document.getElementById("createGoalModal");
  if (modal) {
    modal.classList.add("hidden");
    document.body.style.overflow = ""; // Restore scrolling
    
    // Reset form
    const form = modal.querySelector('form');
    if (form) form.reset();
  }
}

/* ============================================
   UPDATE PROGRESS MODAL FUNCTIONS
   ============================================ */

/**
 * Open the Update Progress modal
 * @param {number} goalId - The ID of the goal to update
 * @param {number} currentProgress - Current progress percentage (0-100)
 */
function openUpdateModal(goalId, currentProgress) {
  const modal = document.getElementById("updateProgressModal");
  const form = document.getElementById("updateProgressForm");
  
  if (!modal || !form) return;

  // Set form action URL
  form.action = `/goals/update-progress/${goalId}/`;

  // Initialize all progress displays
  const currentProgressValue = document.getElementById("currentProgressValue");
  const slider = document.getElementById("progress_slider");
  const input = document.getElementById("progress_input");

  // Set current progress display
  if (currentProgressValue) {
    currentProgressValue.textContent = currentProgress + "%";
  }

  // Set slider and input values
  if (slider) slider.value = currentProgress;
  if (input) input.value = currentProgress;

  // Update all visual elements
  updateProgressDisplay(currentProgress);

  // Show modal
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

/**
 * Close the Update Progress modal
 */
function closeUpdateModal() {
  const modal = document.getElementById("updateProgressModal");
  if (modal) {
    modal.classList.add("hidden");
    document.body.style.overflow = "";
  }
}

/* ============================================
   PROGRESS UPDATE FUNCTIONALITY
   ============================================ */

/**
 * Update all progress display elements
 * @param {number} value - Progress value (0-100)
 */
function updateProgressDisplay(value) {
  // Update visual progress bar
  const visualBar = document.getElementById("visualProgressBar");
  if (visualBar) {
    visualBar.style.width = value + '%';
    
    // Update color class based on progress
    visualBar.className = 'progress-bar-fill';
    if (value >= 75) {
      visualBar.classList.add('high-progress');
    } else if (value >= 50) {
      visualBar.classList.add('medium-progress');
    } else if (value >= 25) {
      visualBar.classList.add('low-progress');
    }
  }
  
  // Update percentage text
  const percentage = document.getElementById("progressPercentage");
  if (percentage) {
    percentage.textContent = value + '%';
  }
  
  // Update new progress value display
  const newValue = document.getElementById("newProgressValue");
  if (newValue) {
    newValue.textContent = value + '%';
  }
  
  // Update circular progress ring
  const progressRing = document.getElementById("progressRingCircle");
  if (progressRing) {
    const circumference = 220; // 2 * PI * 35 (radius)
    const offset = circumference - (value / 100) * circumference;
    progressRing.style.strokeDashoffset = offset;
    
    // Change ring color based on progress
    if (value >= 75) {
      progressRing.setAttribute('stroke', '#16a34a');
    } else if (value >= 50) {
      progressRing.setAttribute('stroke', '#f59e0b');
    } else {
      progressRing.setAttribute('stroke', '#dc2626');
    }
  }
  
  // Update motivational message
  updateMotivationMessage(value);
}

/**
 * Update motivational message based on progress
 * @param {number} value - Progress value (0-100)
 */
function updateMotivationMessage(value) {
  const motivationMsg = document.getElementById("motivationMessage");
  if (!motivationMsg) return;
  
  const messages = {
    0: "🎯 Ready to start? Let's do this!",
    25: "💪 Great start! Keep the momentum going!",
    50: "🚀 Halfway there! You're crushing it!",
    75: "⭐ Almost there! The finish line is in sight!",
    100: "🎉 Amazing! Goal completed! Celebrate this win!"
  };
  
  const msgSpan = motivationMsg.querySelector('span');
  if (msgSpan) {
    if (value >= 75) {
      msgSpan.textContent = messages[100];
    } else if (value >= 50) {
      msgSpan.textContent = messages[75];
    } else if (value >= 25) {
      msgSpan.textContent = messages[50];
    } else if (value > 0) {
      msgSpan.textContent = messages[25];
    } else {
      msgSpan.textContent = messages[0];
    }
  }
}

/**
 * Increment progress by 5%
 */
function incrementProgress() {
  const input = document.getElementById('progress_input');
  const slider = document.getElementById('progress_slider');
  
  if (input && slider) {
    let value = parseInt(input.value) || 0;
    value = Math.min(100, value + 5);
    input.value = value;
    slider.value = value;
    updateProgressDisplay(value);
  }
}

/**
 * Decrement progress by 5%
 */
function decrementProgress() {
  const input = document.getElementById('progress_input');
  const slider = document.getElementById('progress_slider');
  
  if (input && slider) {
    let value = parseInt(input.value) || 0;
    value = Math.max(0, value - 5);
    input.value = value;
    slider.value = value;
    updateProgressDisplay(value);
  }
}

/**
 * Set progress to a specific value (used by preset buttons)
 * @param {number} value - Progress value (0-100)
 */
function setProgress(value) {
  const input = document.getElementById('progress_input');
  const slider = document.getElementById('progress_slider');
  
  if (input && slider) {
    input.value = value;
    slider.value = value;
    updateProgressDisplay(value);
  }
}

/* ============================================
   EVENT LISTENERS
   ============================================ */

document.addEventListener("DOMContentLoaded", function () {
  
  // Sync slider and input for progress modal
  const slider = document.getElementById("progress_slider");
  const input = document.getElementById("progress_input");

  if (slider && input) {
    // Slider changes input
    slider.addEventListener("input", function() {
      input.value = this.value;
      updateProgressDisplay(this.value);
    });

    // Input changes slider
    input.addEventListener("input", function() {
      let value = parseInt(this.value) || 0;
      // Clamp value between 0 and 100
      value = Math.max(0, Math.min(100, value));
      this.value = value;
      slider.value = value;
      updateProgressDisplay(value);
    });
  }

  // Close modal when clicking outside
  const modals = document.querySelectorAll('.goal-overlay');
  modals.forEach(modal => {
    modal.addEventListener('click', function(e) {
      if (e.target === this) {
        if (this.id === 'createGoalModal') {
          closeCreateGoalModal();
        } else if (this.id === 'updateProgressModal') {
          closeUpdateModal();
        }
      }
    });
  });

  // Close modals with Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const createModal = document.getElementById('createGoalModal');
      const updateModal = document.getElementById('updateProgressModal');
      
      if (createModal && !createModal.classList.contains('hidden')) {
        closeCreateGoalModal();
      }
      if (updateModal && !updateModal.classList.contains('hidden')) {
        closeUpdateModal();
      }
    }
  });

  // Form validation for create goal modal
  const createForm = document.querySelector('#createGoalModal form');
  if (createForm) {
    createForm.addEventListener('submit', function(e) {
      const titleInput = this.querySelector('input[name="title"]');
      if (titleInput && !titleInput.value.trim()) {
        e.preventDefault();
        titleInput.focus();
        alert('Please enter a goal title');
      }
    });
  }

  // Form validation for update progress modal
  const updateForm = document.getElementById('updateProgressForm');
  if (updateForm) {
    updateForm.addEventListener('submit', function(e) {
      const progressInput = document.getElementById('progress_input');
      const value = parseInt(progressInput.value);
      
      if (isNaN(value) || value < 0 || value > 100) {
        e.preventDefault();
        alert('Please enter a valid progress value between 0 and 100');
        progressInput.focus();
      }
    });
  }
});

/* ============================================
   EXPORT FUNCTIONS TO WINDOW OBJECT
   Make functions globally accessible
   ============================================ */

window.openCreateGoalModal = openCreateGoalModal;
window.closeCreateGoalModal = closeCreateGoalModal;
window.openUpdateModal = openUpdateModal;
window.closeUpdateModal = closeUpdateModal;
window.incrementProgress = incrementProgress;
window.decrementProgress = decrementProgress;
window.setProgress = setProgress;