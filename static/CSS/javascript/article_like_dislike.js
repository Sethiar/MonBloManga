document.addEventListener("DOMContentLoaded", function() {
    var likeForms = document.querySelectorAll(".like-form");

    likeForms.forEach(function(likeForm) {
        likeForm.addEventListener("submit", function(event) {
            event.preventDefault();
            sendAjaxRequest(likeForm);
        });
    });

    function sendAjaxRequest(form) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", form.action, true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var responseData = JSON.parse(xhr.responseText);
                // Mettre à jour les informations sur les likes et dislikes sur la page
                document.getElementById("articles_likes").innerText = responseData.likes;
                document.getElementById("articles_dislikes").innerText = responseData.dislikes;
                // Afficher un message de confirmation si vous le souhaitez
                alert(responseData.message);
            } else if (xhr.readyState === 4) {
                // Gérer les erreurs de requête
                console.error("Échec de la requête AJAX.");
            }
        };

        var formData = new FormData(form);
        xhr.send(formData);
    }
});