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

/* Share & Flyer Functions */
function sharePage() {
  const shareData = {
    title: document.title,
    text: document.querySelector('meta[name="description"]')?.content || '',
    url: window.location.href
  };
  if (navigator.share) {
    navigator.share(shareData).catch(function() {
      copyToClipboard(window.location.href);
    });
  } else {
    copyToClipboard(window.location.href);
  }
}

function shareFlyer(label, imgSrc) {
  const shareData = {
    title: label + ' | ' + document.title,
    text: label + ' - ' + (document.querySelector('meta[name="description"]')?.content || ''),
    url: window.location.href
  };
  if (navigator.share) {
    navigator.share(shareData).catch(function() {
      copyToClipboard(window.location.href);
    });
  } else {
    copyToClipboard(window.location.href);
  }
}

function copyToClipboard(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function() {
      showToast('Link copied to clipboard!');
    }).catch(function() {
      fallbackCopy(text);
    });
  } else {
    fallbackCopy(text);
  }
}

function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand('copy'); showToast('Link copied to clipboard!'); }
  catch(e) { showToast('Could not copy link.'); }
  document.body.removeChild(ta);
}

function showToast(message) {
  const existing = document.querySelector('.flyer-toast');
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.className = 'flyer-toast';
  toast.textContent = message;
  toast.style.cssText = 'position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1a1a1a;color:#fff;padding:12px 24px;border-radius:8px;z-index:10000;font-family:Inter,sans-serif;font-size:14px;opacity:0;transition:opacity 0.3s;';
  document.body.appendChild(toast);
  requestAnimationFrame(function() { toast.style.opacity = '1'; });
  setTimeout(function() { toast.style.opacity = '0'; setTimeout(function() { toast.remove(); }, 300); }, 2000);
}

function openFlyerLightbox(imgSrc) {
  const overlay = document.createElement('div');
  overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.9);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:20px;';
  overlay.onclick = function() { overlay.remove(); };
  const img = document.createElement('img');
  img.src = imgSrc;
  img.alt = 'Flyer';
  img.style.cssText = 'max-width:90vw;max-height:90vh;object-fit:contain;border-radius:4px;';
  overlay.appendChild(img);
  document.body.appendChild(overlay);
}

/* Init social share links */
(function() {
  var fbLink = document.getElementById('share-facebook');
  var waLink = document.getElementById('share-whatsapp');
  if (fbLink) {
    fbLink.href = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(window.location.href);
  }
  if (waLink) {
    waLink.href = 'https://wa.me/?text=' + encodeURIComponent(document.title + ' ' + window.location.href);
  }
})();
