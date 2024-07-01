document.getElementById('copy-link').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default behavior of the anchor tag
    
    var url = event.target.href; // Get the URL from the href attribute
    var message = "Link copied to clipboard";

    // Copy the URL to the clipboard
    navigator.clipboard.writeText(url)
        .then(function() {
            // Show a message indicating the link has been copied
            alert(message);
        })
        .catch(function() {
            // Handle errors if copying fails
            alert("Failed to copy link to clipboard");
        });
});

