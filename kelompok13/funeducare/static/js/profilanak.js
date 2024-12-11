// Function to show the form for adding or editing a child's profile
function showAddChildForm() {
  // Show the form popup
  document.getElementById("popup-add-child-form").style.display = "block";
  // Show the overlay
  document.getElementById("popup-overlay").style.display = "block";
}

// Function to close the form when clicking outside the popup (overlay)
function closePopup() {
  // Hide the form popup
  document.getElementById("popup-add-child-form").style.display = "none";
  // Hide the overlay
  document.getElementById("popup-overlay").style.display = "none";
}

// Function to cancel the action and close the form
function cancelAddChild() {
  // Reset the form fields (optional if you want to reset the fields on cancel)
  document.getElementById("popup-add-child-form").reset();
  // Hide the form popup and overlay
  closePopup();
}

// Optional: If you want to reset the form fields on clicking the Cancel button, you can use this function above
document
  .querySelector('#popup-add-child-form button[type="button"]')
  .addEventListener("click", cancelAddChild);

// Adding event listener for closing the popup when clicking the overlay
document.getElementById("popup-overlay").addEventListener("click", closePopup);
