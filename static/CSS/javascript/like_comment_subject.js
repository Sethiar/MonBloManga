// Récupérer le jeton CSRF depuis le modèle Flask
    var csrfToken = document.querySelector('#fromlikecomment input[name="csrf_token"]').value;


    function toggleLike(element, commentId, userPseudo) {
    // Ici, vous pouvez utiliser userPseudo directement passé en paramètre
    console.log(`User Pseudo: ${userPseudo}`);
    console.log(`CommentId: ${commentId}`);
    console.log(`csrfToken: ${csrfToken}`);

        // Envoi d'une requête AJAX à Flask pour enregistrer l'utilisateur qui a aimé
            $.ajax({
            type: 'POST',
            url: '/user/likes_comment_subject',
            data: JSON.stringify({ comment_id: commentId, user_pseudo:userPseudo}),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken  // Inclure le jeton CSRF dans les en-têtes de la requête
            },
            success: function(response) {
                console.log('Utilisateur liké enregistré dans la base de données.');
            // Changer l'icône en fonction de l'action (like ou dislike)
            if (element.classList.contains('liked')) {
                // Si l'utilisateur a aimé le commentaire, retire la classe 'liked' et change l'icône
                element.classList.remove('liked');
                element.innerHTML = '&#9825;'; // Icône pour un cœur vide
            } else {
                // Si l'utilisateur n'a pas aimé le commentaire, ajoute la classe 'liked' et change l'icône
                element.classList.add('liked');
                element.innerHTML = '&#9829;'; // Icône pour un cœur plein
            }
        },
        error: function(xhr, status, error) {
            console.error('Erreur lors de l\'enregistrement de l\'utilisateur liké :', error);
        }
    });
}