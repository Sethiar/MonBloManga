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
        url: '/user/likes_comment_article',
        data: JSON.stringify({ comment_id: commentId, user_pseudo: userPseudo }),
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(response) {
            console.log('Utilisateur liké enregistré dans la base de données.');
            const likeCount = response.like_count;
            const userPseudo = response.user_pseudo;
            const likeMessageElement = document.getElementById(`like-message-${commentId}`);
            let message;
            if (response.liked) {
                element.classList.add('liked');
                element.innerHTML = '&#9829;'; // Icône pour un cœur plein
                if (likeCount > 1) {
                    message = `${userPseudo} et ${likeCount - 1} autre(s) personne(s) ont aimé votre commentaire.`;
                } else {
                    message = `Personne n'a aimé votre commentaire pour le moment.`;
                }
            } else {
                element.classList.remove('liked');
                element.innerHTML = '&#9825;'; // Icône pour un cœur vide
                if (likeCount > 1) {
                    message = `Vous et ${likeCount - 1} autre(s) personne(s) ont aimé votre commentaire.`;
                } else if (likeCount === 1) {
                    message = `${userPseudo} a aimé votre commentaire.`;
                } else {
                    message = `Personne n'a aimé votre commentaire pour le moment.`;
                }
            }
            likeMessageElement.innerText = message;
        },
        error: function(xhr, status, error) {
            console.error('Erreur lors de l\'enregistrement de l\'utilisateur liké :', error);
        }
    });
}