// This file contains JavaScript for interactivity on the website. 
// It handles the button clicks to show/hide the respective recruitment options 
// based on the user's selection and includes functionality for toggling 
// between dark and light modes.

document.addEventListener('DOMContentLoaded', function() {
    const techButton = document.getElementById('tech-button');
    const nonTechButton = document.getElementById('non-tech-button');
    const executiveRecruitment = document.getElementById('executive-recruitment');
    const directorateRecruitment = document.getElementById('directorate-recruitment');
    const darkModeToggle = document.getElementById('dark-mode-toggle');

    techButton.addEventListener('click', function() {
        executiveRecruitment.style.display = 'block';
        directorateRecruitment.style.display = 'none';
    });

    nonTechButton.addEventListener('click', function() {
        executiveRecruitment.style.display = 'none';
        directorateRecruitment.style.display = 'block';
    });

    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
    });
});