function openCreateGoalModal() {
  document.getElementById("createGoalModal").classList.remove("hidden");
}

function closeCreateGoalModal() {
  document.getElementById("createGoalModal").classList.add("hidden");
}

function openUpdateModal(goalId, currentProgress) {
  const modal = document.getElementById("updateProgressModal");
  const form = document.getElementById("updateProgressForm");

  document.getElementById("currentProgressDisplay").value = currentProgress + "%";
  document.getElementById("progress_slider").value = currentProgress;
  document.getElementById("progress_input").value = currentProgress;

  form.action = `/goals/update-progress/${goalId}/`;
  modal.classList.remove("hidden");
}

function closeUpdateModal() {
  document.getElementById("updateProgressModal").classList.add("hidden");
}

// Sync slider ↔ input
document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById("progress_slider");
  const input = document.getElementById("progress_input");

  if (slider && input) {
    slider.addEventListener("input", () => input.value = slider.value);
    input.addEventListener("input", () => slider.value = input.value);
  }
});

window.openCreateGoalModal = openCreateGoalModal;
window.closeCreateGoalModal = closeCreateGoalModal;
window.openUpdateModal = openUpdateModal;
window.closeUpdateModal = closeUpdateModal;