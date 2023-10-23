document.addEventListener("DOMContentLoaded", function() {
        var successMessage = document.getElementById("success-message");
        if (successMessage.textContent.trim() !== "") {
            successMessage.style.display = "block";
        }
    });