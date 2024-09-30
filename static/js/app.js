document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById(' user-input').value;
    const fileInput = document.getElementById('file-input').files[0];
    const chatHistory = document.getElementById('chat-history');

    if (userInput) {
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            chatHistory.innerHTML += `<div class="message user-message">${userInput}</div>`;
            chatHistory.innerHTML += `<div class="message bot-message">${data.response}</div>`;
            chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the bottom
        });

        document.getElementById('user-input').value = '';
    }

    if (fileInput) {
        const formData = new FormData();
        formData.append('file', fileInput);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            chatHistory.innerHTML += `<div class="message user-message">Uploaded: ${fileInput.name}</div>`;
            chatHistory.innerHTML += `<div class="message bot-message">${data.description}</div>`;
            chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the bottom
        });

        document.getElementById('file-input').value = '';
    }
});
