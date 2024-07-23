document.getElementById('send-button').addEventListener('click', () => {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        addMessage(userInput, 'user-message');
        fetchResponse(userInput);
        document.getElementById('user-input').value = '';
    }
});

function addMessage(text, className) {
    const message = document.createElement('div');
    message.className = `message ${className}`;
    message.textContent = text;
    document.getElementById('chat-log').appendChild(message);
    document.getElementById('chat-log').scrollTop = document.getElementById('chat-log').scrollHeight;
}

async function fetchResponse(userInput) {
    // Replace with your backend endpoint
    const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    const botResponse = data.response;
    addMessage(botResponse, 'bot-message');
}
