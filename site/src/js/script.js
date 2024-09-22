document.getElementById('uploadBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('fileInput');
    const loadingMessage = document.getElementById('loadingMessage');
    const timeRemaining = document.getElementById('timeRemaining');

    if (fileInput.files.length === 0) {
        alert('Please select a file.');
        return;
    }

    loadingMessage.style.display = 'flex';
    let countdown = 10;

    const countdownInterval = setInterval(() => {
        countdown--;
        timeRemaining.textContent = countdown;
        if (countdown <= 0) {
            clearInterval(countdownInterval);
        }
    }, 1000); // Update every second

    setTimeout(async () => {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('http://127.0.0.1:8000/pe_scan/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                },
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Error uploading the file.');
            }

            const data = await response.json();
            displayResults(data.results);
        } catch (error) {
            alert(error.message);
        } finally {
            loadingMessage.style.display = 'none';
            fileInput.value = ''; // Reset input field
        }
    }, 10000); // Wait for 10 seconds
});

function displayResults(results) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `<h2>Analysis Results</h2>
                           <p><strong>Classification:</strong> ${results.classification}</p>
                           <p><strong>Features:</strong></p>
                           <ul id="featuresList"></ul>`;
    
    const featuresList = document.getElementById('featuresList');
    
    Object.entries(results.features).forEach(([key, value]) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<strong>${key}:</strong> <span class="animated-number">${value}</span>`;
        featuresList.appendChild(listItem);
    });

    resultDiv.style.display = 'block';
}
