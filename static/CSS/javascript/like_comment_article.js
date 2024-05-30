let likedComments = {}; // Dictionnaire pour stocker les likes de chaque commentaire

function toggleLike(element) {
    const commentElement = element.closest('.comment');
    const commentId = commentElement.getAttribute('data-comment-id');
    const currentUser = document.querySelector('meta[name="current-user"]').getAttribute('content');

    if (!commentId) {
        return; // S'assure que chaque commentaire a un ID
    }

    const usersList = likedComments[commentId] || [];
    const userIndex = usersList.indexOf(currentUser);
    const likeCountElement = element.nextElementSibling;
    const likedUsersElement = likeCountElement.nextElementSibling;

    const liked = userIndex === -1;
    
    if (liked) {
        usersList.push(currentUser);
        element.classList.add('liked');
    } else {
        usersList.splice(userIndex, 1);
        element.classList.remove('liked');
    }

    likedComments[commentId] = usersList;
    likeCountElement.textContent = usersList.length;
    likedUsersElement.textContent = 'Liked by: ' + usersList.join(', ');

    // Appel AJAX pour mettre à jour le backend
    updateLikeInDatabase(commentId, currentUser, liked);
}

function updateLikeInDatabase(commentId, userId, liked) {
    fetch(`/like_comment`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(), // Inclure le token CSRF pour la sécurité
        },
        body: JSON.stringify({ commentId, userId, liked })
    });
}

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

document.addEventListener('DOMContentLoaded', () => {
    const comments = document.querySelectorAll('.comment');
    comments.forEach((comment, index) => {
        const id = 'comment-' + (index + 1);
        comment.setAttribute('data-comment-id', id);
        likedComments[id] = [];
    });
});