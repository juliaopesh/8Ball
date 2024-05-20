document.addEventListener("DOMContentLoaded", function() {
    var startGameButton = document.getElementById("startGameButton");
    var player1NameInput = document.getElementById("player1Name");
    var player2NameInput = document.getElementById("player2Name");

    startGameButton.addEventListener("click", function() {
        var player1Name = player1NameInput.value.trim();
        var player2Name = player2NameInput.value.trim();

        // Check if both player names are filled
        if (player1Name === "" || player2Name === "") {
            alert("Please enter both players' names.");
            return;
        }

        // Create a FormData object to send data with the POST request
        var formData = new FormData();
        formData.append("player1Name", player1Name);
        formData.append("player2Name", player2Name);

        // Send a POST request to the server
        fetch("/index.html", {
            method: "POST",
            body: formData
        })
        .then(response => {
            // Handle response from the server
            if (response.ok) {
                // Redirect to the pool.html page
                window.location.href = "pool.html";
            } else {
                alert("Error starting the game.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error starting the game.");
        });
    });
});
