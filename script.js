// Additional JavaScript functionality

// Function to handle smooth reveal of elements as they come into view
function initScrollReveal() {
    const revealElements = document.querySelectorAll(".reveal")
  
    const revealOptions = {
      threshold: 0.15,
      rootMargin: "0px 0px -50px 0px",
    }
  
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed")
          revealObserver.unobserve(entry.target)
        }
      })
    }, revealOptions)
  
    revealElements.forEach((element) => {
      revealObserver.observe(element)
      // Add initial hidden state in CSS
      element.classList.add("reveal-hidden")
    })
  }
  
  // Function to initialize image comparison slider
  function initImageComparison() {
    const comparisonContainers = document.querySelectorAll(".comparison-container")
  
    comparisonContainers.forEach((container) => {
      const slider = container.querySelector(".comparison-slider")
  
      function moveSlider(x) {
        let position = x - container.getBoundingClientRect().left
        if (position < 0) position = 0
        if (position > container.offsetWidth) position = container.offsetWidth
  
        const percentage = (position / container.offsetWidth) * 100
        slider.style.left = `${percentage}%`
  
        const beforeImage = container.querySelector(".before-image")
        beforeImage.style.width = `${percentage}%`
      }
  
      // Mouse events
      container.addEventListener("mousemove", (e) => {
        moveSlider(e.pageX)
      })
  
      // Touch events
      container.addEventListener("touchmove", (e) => {
        moveSlider(e.touches[0].pageX)
      })
  
      // Initialize slider position
      moveSlider(container.getBoundingClientRect().left + container.offsetWidth / 2)
    })
  }
  
  // Function to handle mobile navigation
  function initMobileNav() {
    const menuToggle = document.querySelector(".menu-toggle")
    const mobileNav = document.querySelector(".mobile-nav")
  
    if (menuToggle && mobileNav) {
      menuToggle.addEventListener("click", () => {
        mobileNav.classList.toggle("active")
        menuToggle.classList.toggle("active")
      })
  
      // Close mobile nav when clicking outside
      document.addEventListener("click", (e) => {
        if (!mobileNav.contains(e.target) && !menuToggle.contains(e.target)) {
          mobileNav.classList.remove("active")
          menuToggle.classList.remove("active")
        }
      })
    }
  }
  
  // Initialize all functions when DOM is loaded
  document.addEventListener("DOMContentLoaded", () => {
    initScrollReveal()
    initImageComparison()
    initMobileNav()
  
    // Add parallax effect to hero section
    window.addEventListener("scroll", () => {
      const scrollPosition = window.pageYOffset
      const parallaxElements = document.querySelectorAll(".parallax")
  
      parallaxElements.forEach((element) => {
        const speed = element.getAttribute("data-speed") || 0.5
        element.style.transform = `translateY(${scrollPosition * speed}px)`
      })
    })
  })
  
  