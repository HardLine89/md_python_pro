document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".vote-btn").forEach(button => {
        button.addEventListener("click", function () {
            let articleId = this.dataset.article;
            let action = this.dataset.action;
            let likeBtn = document.querySelector(`[data-article="${articleId}"][data-action="like"]`);
            let dislikeBtn = document.querySelector(`[data-article="${articleId}"][data-action="dislike"]`);

            fetch(`/article/${articleId}/vote/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ action: action })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById("like-count").textContent = data.likes;
                    document.getElementById("dislike-count").textContent = data.dislikes;

                    if (data.user_vote === 1) {
                        likeBtn.classList.remove("btn-outline-success");
                        likeBtn.classList.add("btn-success");

                        dislikeBtn.classList.remove("btn-danger");
                        dislikeBtn.classList.add("btn-outline-danger");
                    } else if (data.user_vote === -1) {
                        dislikeBtn.classList.remove("btn-outline-danger");
                        dislikeBtn.classList.add("btn-danger");

                        likeBtn.classList.remove("btn-success");
                        likeBtn.classList.add("btn-outline-success");
                    } else {
                        // Если голос снят, возвращаем обе кнопки в outline-режим
                        likeBtn.classList.remove("btn-success");
                        likeBtn.classList.add("btn-outline-success");

                        dislikeBtn.classList.remove("btn-danger");
                        dislikeBtn.classList.add("btn-outline-danger");
                    }
                } else {
                    console.error("Ошибка:", data.error);
                }
            })
            .catch(error => console.error("Ошибка сети:", error));
        });
    });
});

function getCsrfToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}