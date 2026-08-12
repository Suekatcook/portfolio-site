(function () {
  "use strict";

  function initFadeRise() {
    var items = document.querySelectorAll(".fade-rise");
    if (!items.length) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      items.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    items.forEach(function (el, index) {
      el.style.transitionDelay = index * 0.15 + "s";
      observer.observe(el);
    });
  }

  function initDesignGalleries() {
    document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
      var images = gallery.querySelectorAll("img");
      var dotsWrap = gallery.parentElement.querySelector(".gallery-dots");
      if (!images.length) return;

      var index = 0;
      var timer;

      function show(i) {
        images.forEach(function (img, n) {
          img.classList.toggle("active", n === i);
        });
        if (dotsWrap) {
          dotsWrap.querySelectorAll("button").forEach(function (btn, n) {
            btn.classList.toggle("active", n === i);
          });
        }
        index = i;
      }

      if (dotsWrap) {
        images.forEach(function (_img, n) {
          var btn = document.createElement("button");
          btn.type = "button";
          btn.setAttribute("aria-label", "Show image " + (n + 1));
          btn.addEventListener("click", function () {
            show(n);
            restart();
          });
          dotsWrap.appendChild(btn);
        });
      }

      function next() {
        show((index + 1) % images.length);
      }

      function restart() {
        clearInterval(timer);
        timer = setInterval(next, 4000);
      }

      show(0);
      restart();
    });
  }

  function initLightbox() {
    var lightbox = document.getElementById("lightbox");
    if (!lightbox) return;

    var img = lightbox.querySelector("img");
    var captionDiv = lightbox.querySelector("#lightbox-caption");
    var current = 0;
    var items = [];

    // 1. Bind to drawing items
    document.querySelectorAll(".drawing-item").forEach(function (btn, i) {
      btn.addEventListener("click", function () {
        items = Array.from(document.querySelectorAll(".drawing-item img"));
        openAt(i);
      });
    });

    // 2. Bind to design galleries
    document.querySelectorAll(".design-gallery").forEach(function (gallery) {
      gallery.addEventListener("click", function () {
        var images = Array.from(gallery.querySelectorAll("img"));
        var captions = Array.from(gallery.querySelectorAll(".caption"));
        
        // Map images to an array of objects containing src, alt, and caption
        items = images.map(function(imageEl, idx) {
            return {
                src: imageEl.src,
                alt: imageEl.alt,
                caption: captions[idx] ? captions[idx].textContent : ""
            };
        });

        var activeImg = gallery.querySelector("img.active");
        var activeIndex = images.indexOf(activeImg);
        openAt(activeIndex);
      });
    });

    function openAt(i) {
      if (i < 0 || !items.length) return;
      current = i;
      
      // Handle both raw DOM elements (drawings) and mapped objects (design)
      var currentItem = items[current];
      img.src = currentItem.src || currentItem.querySelector("img").src;
      img.alt = currentItem.alt || currentItem.querySelector("img").alt;
      
      if (captionDiv) {
          captionDiv.textContent = currentItem.caption || "";
      }

      lightbox.classList.add("open");
      lightbox.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }

    function close() {
      lightbox.classList.remove("open");
      lightbox.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }

    function step(delta) {
      if (!items.length) return;
      current = (current + delta + items.length) % items.length;
      openAt(current);
    }

    lightbox.querySelector(".lightbox-close").addEventListener("click", close);
    lightbox.querySelector(".lightbox-prev").addEventListener("click", function () { step(-1); });
    lightbox.querySelector(".lightbox-next").addEventListener("click", function () { step(1); });

    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) close();
    });

    document.addEventListener("keydown", function (e) {
      if (!lightbox.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFadeRise();
    initDesignGalleries();
    initLightbox();
  });
})();
