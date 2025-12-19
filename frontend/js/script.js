document.addEventListener('DOMContentLoaded', function() {
    // "Read More" functionality (general)
    const readMoreLinks = document.querySelectorAll('.read-more');

    readMoreLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const parentElement = this.parentNode;
            const fullText = parentElement.querySelector('.full-text');
            const shortText = parentElement.querySelector('.short-text');

            if (fullText && shortText) {
                shortText.style.display = 'none';
                fullText.style.display = 'block';
                this.style.display = 'none';
            }
        });
    });

    // Basic client-side search (can be enhanced with AJAX)
//     const searchInput = document.querySelector('.search-bar input[type="text"]');
//     const searchResultsContainer = document.querySelector('.search-bar ul');
//     const allSearchableElements = document.querySelectorAll('.consultant-card, .card'); // Adjust selectors as needed

//     if (searchInput && searchResultsContainer && allSearchableElements.length > 0) {
//         searchInput.addEventListener('input', function() {
//             const searchTerm = this.value.toLowerCase();
//             searchResultsContainer.innerHTML = '';
//             let matchingResults = [];

//             allSearchableElements.forEach(element => {
//                 let textToSearch = '';
//                 if (element.querySelector('h4 a')) {
//                     textToSearch += element.querySelector('h4 a').textContent.toLowerCase() + ' ';
//                 } else if (element.querySelector('h3 a')) {
//                     textToSearch += element.querySelector('h3 a').textContent.toLowerCase() + ' ';
//                 } else if (element.querySelector('h4')) {
//                     textToSearch += element.querySelector('h4').textContent.toLowerCase() + ' ';
//                 } else if (element.querySelector('h3')) {
//                     textToSearch += element.querySelector('h3').textContent.toLowerCase() + ' ';
//                 }
//                 if (element.querySelector('p')) {
//                     textToSearch += element.querySelector('p').textContent.toLowerCase() + ' ';
//                 }

//                 if (textToSearch.includes(searchTerm)) {
//                     // Basic display - you might want to extract relevant info
//                     const listItem = document.createElement('li');
//                     let link = element.querySelector('a');
//                     listItem.textContent = link ? link.textContent : (element.querySelector('h4') ? element.querySelector('h4').textContent : (element.querySelector('h3') ? element.querySelector('h3').textContent : ''));
//                     if (link && link.href) {
//                         const anchor = document.createElement('a');
//                         anchor.href = link.href;
//                         anchor.textContent = listItem.textContent;
//                         listItem.innerHTML = '';
//                         listItem.appendChild(anchor);
//                     }
//                     searchResultsContainer.appendChild(listItem);
//                 }
//             });

//             searchResultsContainer.style.display = matchingResults.length > 0 && searchTerm ? 'block' : 'none';
//         });
//     }
});