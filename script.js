document.getElementById('newsForm').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const newsUrl = document.getElementById('newsUrl').value;
    
    fetch('/api/summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: newsUrl })
    })
    .then(response => response.json())
    .then(data => {
        const summaryResult = document.getElementById('summaryResult');
        summaryResult.innerHTML = `<h2>Summary</h2><p>${data.summary}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
