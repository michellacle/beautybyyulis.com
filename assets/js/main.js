const menuButton = document.querySelector("[data-menu-button]");
const navLinks = document.querySelector("[data-nav-links]");

if (menuButton && navLinks) {
  menuButton.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("is-open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });
}

const contactForm = document.querySelector("[data-contact-form]");

if (contactForm) {
  const formStatus = document.querySelector("[data-form-status]");

  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = {};
    contactForm.querySelectorAll("input, select, textarea").forEach((input) => {
      if (!input.name) return;
      formData[input.name] = input.value.trim();
    });

    const submitButton = contactForm.querySelector('button[type="submit"]');
    const isSpanish = document.documentElement.lang === "es";

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = isSpanish ? "Enviando..." : "Submitting...";
    }

    if (formStatus) {
      formStatus.style.display = "block";
      formStatus.style.color = "#6b6259";
      formStatus.textContent = isSpanish ? "Enviando..." : "Submitting...";
    }

    fetch("https://thinksmart.life/forms/beautybyyulis/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((result) => {
        if (!result.success) {
          throw new Error(result.message || "Submission failed");
        }

        if (formStatus) {
          formStatus.style.color = "#198754";
          formStatus.textContent = isSpanish
            ? "¡Gracias! Hemos recibido su solicitud. Nos pondremos en contacto pronto."
            : "Thank you! Your request has been received. We will be in touch shortly.";
        }
        contactForm.reset();
      })
      .catch((error) => {
        if (formStatus) {
          formStatus.style.color = "#dc3545";
          formStatus.textContent = isSpanish
            ? "Lo sentimos, hubo un problema al enviar su solicitud. Por favor, envíanos un correo a beautybyyulis@gmail.com o inténtalo de nuevo."
            : "Sorry, there was a problem submitting your request. Please email us directly at beautybyyulis@gmail.com or try again.";
        }
        console.error("Form submission error:", error);
      })
      .finally(() => {
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.textContent = isSpanish ? "Enviar Solicitud" : "Send Request";
        }
      });
  });
}
