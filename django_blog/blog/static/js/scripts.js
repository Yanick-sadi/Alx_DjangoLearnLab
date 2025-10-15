// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');
    
    // Add any interactive functionality here
    const articles = document.querySelectorAll('article');
    articles.forEach(article => {
        article.addEventListener('click', function() {
            this.style.backgroundColor = '#f0f0f0';
        });
    });
});