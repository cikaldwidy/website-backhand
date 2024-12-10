document.addEventListener("DOMContentLoaded", function () {
  const faqItems = document.querySelectorAll(".faq-item");

  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");

    question.addEventListener("click", () => {
      const isActive = question.classList.contains("active");

      // Tutup semua jawaban terbuka lainnya
      faqItems.forEach((otherItem) => {
        if (otherItem !== item) {
          otherItem.querySelector(".faq-question").classList.remove("active");
          otherItem.querySelector(".faq-answer").classList.remove("active");
        }
      });

      // Alihkan item yang diklik
      question.classList.toggle("active", !isActive);
      answer.classList.toggle("active", !isActive);
    });
  });
});
// Penanganan pengiriman formulir
const contactForm = document.querySelector(
  'form[aria-labelledby="contact-form"]'
);

if (contactForm) {
  contactForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Mencegah pengiriman formulir secara default

    // Ambil nilai dari formulir
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const contact = document.getElementById("contact").value;
    const message = document.getElementById("message").value;

    // Di sini biasanya Anda akan mengirim data ini ke server
    // Untuk saat ini, kita hanya akan mencetaknya ke konsol
    console.log("Form submitted:", { name, email, contact, message });

    // Tampilkan pesan sukses (Anda bisa mengganti ini dengan modal atau umpan balik UI lainnya)
    alert(
      "Terima kasih! Pesan Anda telah terkirim. Kami akan segera menghubungi Anda."
    );

    // Reset formulir setelah pengiriman
    contactForm.reset();
  });
}

// Scroll halus untuk tautan jangkar
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault(); // Mencegah perilaku default tautan

    // Gulir halus ke elemen yang dituju
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
    });
  });
});

// Perilaku gulir navbar
const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {
  // Tambahkan kelas 'scrolled' pada navbar saat halaman digulir lebih dari 50px
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled"); // Hapus kelas jika kurang dari 50px
  }
});
