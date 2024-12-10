// JavaScript for showing/hiding the modals

function showDetails() {
  const popupDetail = document.getElementById("popup-detail");
  const overlay = document.getElementById("popup-overlay");

  popupDetail.classList.add("active");
  overlay.style.display = "block";
}

function closePopup() {
  // Hide the detail modal and overlay
  const popupDetail = document.getElementById("popup-detail");
  const overlay = document.getElementById("popup-overlay");

  popupDetail.classList.remove("active");
  overlay.style.display = "none";
}

function showAddChildForm() {
  // Show the Add Child Form popup
  const popupAddChildForm = document.getElementById("popup-add-child-form");
  const overlay = document.getElementById("popup-overlay");

  popupAddChildForm.style.display = "block";
  overlay.style.display = "block";
}

function cancelAddChild() {
  // Hide the Add Child Form popup and overlay
  const popupAddChildForm = document.getElementById("popup-add-child-form");
  const overlay = document.getElementById("popup-overlay");

  popupAddChildForm.style.display = "none";
  overlay.style.display = "none";
}

// Close popup if clicking outside the popup area (on overlay)
document.getElementById("popup-overlay").addEventListener("click", closePopup);
