let rawEmailBody = ''; // Store the raw HTML body globally

function generateEmail() {
    const prompt = document.getElementById('prompt').value;
    const tone = document.getElementById('tone').value;
    const detail_level = document.getElementById('detail_level').value;
    const to = document.getElementById('to').value;
    
    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            prompt, 
            tone, 
            detail_level,
            recipient_name: to,
            sender_name: 'Mayank'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.subject && data.body) {
            document.getElementById('subject').value = data.subject;
            rawEmailBody = data.body; // Store raw HTML with <br> tags
            document.getElementById('body').value = data.body.replace(/<br>/g, '\n'); // Display with newlines
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => alert('Failed to generate email: ' + error));
}

function generateReply(thread_id) {
    const prompt = document.getElementById('prompt').value;
    const tone = document.getElementById('tone').value;
    const detail_level = document.getElementById('detail_level').value;
    const to = document.getElementById('to').value;
    
    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            prompt, 
            tone, 
            detail_level, 
            thread_id,
            recipient_name: to,
            sender_name: 'Mayank'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.subject && data.body) {
            document.getElementById('subject').value = data.subject;
            rawEmailBody = data.body; // Store raw HTML with <br> tags
            document.getElementById('body').value = data.body.replace(/<br>/g, '\n'); // Display with newlines
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => alert('Failed to generate reply: ' + error));
}

function formatText(style) {
    const textarea = document.getElementById('body');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);
    let formattedText = style === 'bold' ? `<b>${selectedText}</b>` : `<i>${selectedText}</i>`;
    textarea.value = textarea.value.substring(0, start) + formattedText + textarea.value.substring(end);
    rawEmailBody = textarea.value.replace(/\n/g, '<br>'); // Update raw body with HTML tags
}

function updateFont() {
    const font = document.getElementById('font_type').value;
    document.getElementById('body').style.fontFamily = font;
}

// Override form submission to use raw HTML body
document.querySelector('form').addEventListener('submit', function(e) {
    const bodyInput = document.getElementById('body');
    bodyInput.value = rawEmailBody; // Set the form value to raw HTML before submission
});