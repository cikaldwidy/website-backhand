$(document).ready(function () {
  // Disable submit button initially
  $('button[type="submit"]').prop("disabled", true);

  // Listen for checkbox changes
  $("#termsCheckbox").change(function () {
    if ($(this).is(":checked")) {
      $('button[type="submit"]').prop("disabled", false);
    } else {
      $('button[type="submit"]').prop("disabled", true);
    }
  });
});

// jQuery untuk menangani event klik tombol Cancel
$("#cancelButton").on("click", function () {
  window.location.href = "index.html"; // Pastikan path sesuai
});

// jQuery untuk menangani pengiriman form
$("#bookingForm").on("submit", function (event) {
  // Tidak perlu event.preventDefault(); karena kita ingin mengirimkan form ke server Django
  let isValid = true;

  // Validasi field
  $("#bookingForm input, #bookingForm select").each(function () {
    if (!$(this).val()) {
      alert("Mohon isi semua field yang diperlukan!");
      isValid = false;
      return false; // Keluar dari loop jika ada field yang kosong
    }
  });

  if (!isValid) {
    event.preventDefault(); // Hentikan pengiriman jika validasi gagal
  } else {
    // Biarkan form terkirim ke server Django
    alert("Form berhasil dikirim!");
  }
});
