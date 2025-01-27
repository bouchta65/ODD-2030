document.getElementById('importButton').addEventListener('click', function() {
    // Trigger file input dialog
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    // File has been selected
    var file = this.files[0];
    
    // Check if file is selected
    if (file) {
        // Create FormData object
        var formData = new FormData();
        formData.append('file', file);

        // Send AJAX request to Flask route to import the file
        fetch('/import-data', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle response from Flask route
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
