async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('transcription').textContent = data.transcription;
        document.getElementById('summary').textContent = data.summary;
        const actionItems = document.getElementById('action-items');
        actionItems.innerHTML = data.action_items.split('\n').map(item => `<li>${item}</li>`).join('');
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing the file');
    }
}