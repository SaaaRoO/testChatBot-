async function sendMessage(event) {
    event.preventDefault();
    const userInput = document.getElementById('user-input').value;
    const fileInput = document.getElementById('file-input').files[0];
    
    // Display user message
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="message user-message">${userInput}</div>`;
    document.getElementById('user-input').value = '';

    // Handle file upload if a file is selected
    if (fileInput) {
        const formData = new FormData();
        formData.append('file', fileInput);
        await uploadFile(formData);
    }

    // Send user input to the server
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: userInput })
    });

    const data = await response.json();
    if (data.response) {
        chatBox.innerHTML += `<div class="message ai-message">${data.response}</div>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

async function uploadFile(formData) {
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    // Handle file upload response if necessary
    if (data.message) {
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML += `<div class="message file-message">${data.message}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }
}
