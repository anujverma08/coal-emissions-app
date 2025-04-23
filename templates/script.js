// Emissions Chart
var ctx = document.getElementById('emissionsChart').getContext('2d');
var emissionsChart = new Chart(ctx, {
    type: 'line',  // You can change to 'bar', 'doughnut', etc.
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [{
            label: 'Total Emissions (tons)',
            data: [12000, 15000, 14000, 13000, 16000, 17000],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Activity Breakdown Chart
var ctx2 = document.getElementById('activityChart').getContext('2d');
var activityChart = new Chart(ctx2, {
    type: 'pie',  // Pie chart for activity breakdown
    data: {
        labels: ['Excavation', 'Transportation', 'Equipment Usage', 'Other'],
        datasets: [{
            data: [40, 25, 20, 15],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56', '#4bc0c0']
        }]
    },
    options: {
        responsive: true
    }
});



//slider script
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;

// Function to show the slide
function showSlide(index) {
    const slider = document.querySelector('.slides');
    if (index >= totalSlides) {
        currentSlide = 0;
    } else if (index < 0) {
        currentSlide = totalSlides - 1;
    } else {
        currentSlide = index;
    }
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;
}

// Event listeners for the navigation buttons
document.querySelector('.prev').addEventListener('click', () => {
    showSlide(currentSlide - 1);
});

document.querySelector('.next').addEventListener('click', () => {
    showSlide(currentSlide + 1);
});

// Auto-play the slider every 5 seconds
setInterval(() => {
    showSlide(currentSlide + 1);
}, 5000);
