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

$(document).ready(function () {
  // Fungsi untuk mengecek form terisi
  function checkFormValidity() {
    var namaAnak = $("#id_nama_anak").val();
    var program = $("#id_program").val();
    var fee = $("#id_fee").val();
    var termsChecked = $("#termsCheckbox").is(":checked");

    if (namaAnak && program && fee && termsChecked) {
      $("#bookingButton").prop("disabled", false);
    } else {
      $("#bookingButton").prop("disabled", true);
    }
  }

  // Panggil fungsi saat form berubah
  $("#id_nama_anak, #id_program, #id_fee, #termsCheckbox").on(
    "change",
    function () {
      checkFormValidity();
    }
  );

  // Custom validation saat submit
  $("#bookingForm").on("submit", function (e) {
    var namaAnak = $("#id_nama_anak").val();
    var program = $("#id_program").val();
    var fee = $("#id_fee").val();
    var termsChecked = $("#termsCheckbox").is(":checked");

    if (!namaAnak || !program || !fee || !termsChecked) {
      e.preventDefault();
      alert("Silakan lengkapi semua field dan centang persetujuan");
    }
  });
});
