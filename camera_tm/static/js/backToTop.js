document.addEventListener('DOMContentLoaded', function() {
      const backToTopButton = document.querySelector('#back-to-top');
      if (!backToTopButton) {
          console.error('Back to Top button not found');
          return;
      }

      // Check if the button contains an SVG path (if the design requires it)
      const path = backToTopButton.querySelector('svg path');
      let pathLength = 0;
      if (path) {
          pathLength = path.getTotalLength();
          path.style.strokeDasharray = pathLength + ' ' + pathLength;
          path.style.strokeDashoffset = pathLength;
      }

      window.addEventListener('scroll', function() {
          if (window.scrollY > 300) {
              backToTopButton.style.display = 'block';
          } else {
              backToTopButton.style.display = 'none';
          }

          if (path) {
              const scrollPercentage = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
              const drawLength = pathLength * scrollPercentage;
              path.style.strokeDashoffset = pathLength - drawLength;
          }
      });

      backToTopButton.addEventListener('click', function() {
          window.scrollTo({ top: 0, behavior: 'smooth' });
      });
  });