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
        url: '/user/likes-commentaire-sujet',
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
                    message = `${userPseudo} et ${likeCount - 1} autre(s) utilisateur(s) ont aimé le commentaire.`;
                } else {
                    message = `${userPseudo} a aimé le commentaire.`;
                }
            } else {
                element.classList.remove('liked');
                element.innerHTML = '&#9825;'; // Icône pour un cœur vide
                if (likeCount > 1) {
                    message = `${likeCount} utilisateurs ont aimé le commentaire.`;
                } else if (likeCount === 1) {
                    message = `${likeCount} utilisateur a aimé le commentaire.`;
                } else {
                    message = `Personne n'a aimé le commentaire pour le moment.`;
                }
            }
            likeMessageElement.innerText = message;
        },
        error: function(xhr, status, error) {
            console.error('Erreur lors de l\'enregistrement de l\'utilisateur liké :', error);
        }
    });
}

