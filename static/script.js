// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const classifyBtn = document.getElementById('classify-btn');
    const smsInput = document.getElementById('sms-input');
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');

    classifyBtn.addEventListener('click', async () => {
        const smsText = smsInput.value.trim();
        if (smsText === '') {
            alert('Please enter an SMS message.');
            return;
        }

        // Show loader and clear previous results
        loader.style.display = 'block';
        resultsContainer.innerHTML = '';

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sms_text: smsText }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            resultsContainer.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            console.error('There was a problem with the fetch operation:', error);
        } finally {
            // Hide loader
            loader.style.display = 'none';
        }
    });

    function displayResults(data) {
        // The result from the pipeline includes the original sequence
        const labels = data.labels;
        const scores = data.scores;

        let htmlContent = '<h3>Classification Results:</h3>';
        
        labels.forEach((label, index) => {
            const scorePercent = (scores[index] * 100).toFixed(2);
            htmlContent += `
                <div class="result-item">
                    <span class="result-label">${label}</span>
                    <span class="result-score">${scorePercent}%</span>
                </div>
            `;
        });

        resultsContainer.innerHTML = htmlContent;
    }
});