<script>
        const slides = document.querySelector('.slides');
        const slideImages = document.querySelectorAll('.slide');
        let currentIndex = 0;
        const totalSlides = slideImages.length;
        const slideWidth = 100; // in percentage
        const delay = 6000; // 6 seconds

        // Function to move to the next slide
        function moveToNextSlide() {
            currentIndex = (currentIndex + 1) % totalSlides;
            slides.style.transform = translateX(-${currentIndex * slideWidth}%);
        }

        // Function to move to the previous slide
        function moveToPrevSlide() {
            currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
            slides.style.transform = translateX(-${currentIndex * slideWidth}%);
        }

        // Set up automatic slide show
        setInterval(moveToNextSlide, delay);

        // Event listeners for navigation buttons
        document.querySelector('.prev').addEventListener('click', moveToPrevSlide);
        document.querySelector('.next').addEventListener('click', moveToNextSlide);
        
    </script>