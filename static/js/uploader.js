var form = document.getElementById("upload-form");

form.addEventListener("submit", function (event) {
    event.preventDefault();
    var fileInput = document.getElementById("imagefile");
    var file = fileInput.files[0];

    var formData = new FormData();
    formData.append("imagefile", file);

    // Create a new fetch request
    var request = new Request("/upload", {
        method: "POST",
        body: formData
    });

    // Send the request
    fetch(request)
        .then(function (response) {
            // Check if the request is successful
            if (response.ok) {
                return response.text();
            } else {
                throw new Error("Something went wrong");
            }
        })
        .then(function (text) {
            // Handle the response text
            console.log(text);
        })
        .catch(function (error) {
            // Handle the error
            console.log(error);
        });

    // Get the progress bar element
    var progressBar = document.getElementById("progress-bar");

    // Listen for the progress event on the request
    request.upload.addEventListener("progress", function (event) {
        // Check if the total size is available

            // Calculate the percentage
            var percent = Math.round((event.loaded / event.total) * 100);

            // Update the progress bar
            progressBar.style.width = percent + "%";
            progressBar.textContent = percent + "%";
        
    });
});

