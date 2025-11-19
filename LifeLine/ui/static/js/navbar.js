// Logout confirmation modal
document.addEventListener("DOMContentLoaded", function () {
  const logoutLink = document.querySelector(".logout-link");
  const modal = document.getElementById("logoutModal");
  const cancelBtn = document.getElementById("cancelLogout");

  if (logoutLink && modal && cancelBtn) {
    logoutLink.addEventListener("click", function (e) {
      e.preventDefault();
      modal.classList.add("active");
    });

    cancelBtn.addEventListener("click", function () {
      modal.classList.remove("active");
    });

    modal.addEventListener("click", function (e) {
      if (e.target === modal) modal.classList.remove("active");
    });
  }
});