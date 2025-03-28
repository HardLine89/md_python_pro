document.addEventListener("DOMContentLoaded", function () {
    // Привязываем обработчик события для отправки комментария
    let commentForm = document.getElementById("comment-form");

    if (commentForm) {
        commentForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let text = this.querySelector("textarea").value;
            let articleId = this.dataset.articleId;

            if (!text.trim()) {
                alert("Комментарий не может быть пустым!");
                return;
            }

            fetch(`/article/${articleId}/comment/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({text: text})
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Создаем новый HTML для комментария
                        let commentHtml = `
                        <div class="d-flex align-items-start mb-4">
                            <div class="rounded-circle overflow-hidden" style="width: 40px; height: 40px;">
                                <img src="${data.avatar_url}" class="img-fluid" alt="${data.author}">
                            </div>
                            <div class="ms-3 flex-grow-1">
                                <div class="d-flex align-items-center mb-1">
                                    <span class="badge badge-secondary fw-bold mb-0 me-2">${data.author}</span>
                                    <p class="text-muted mb-0" style="font-size: 0.85rem;">
                                        <i class="fa-solid fa-calendar"></i> ${data.created_at}
                                    </p>
                                </div>
                                <p class="mb-0">${data.text}</p>
                            </div>
                        </div>
                        <hr class="hr">`;

                        // Добавляем новый комментарий в список
                        document.getElementById("comments").innerHTML += commentHtml;
                        this.querySelector("textarea").value = ""; // Очищаем поле ввода
                    } else {
                        alert("Ошибка: " + data.error);
                    }
                })
                .catch(error => console.error("Ошибка сети:", error));
        });
    }

    // Привязываем обработчик для показа/скрытия формы ответа
    // Функция для отображения формы ответа
    window.showReplyForm = function (commentId) {

        let replyForm = document.getElementById(`reply-form-${commentId}`);

        if (replyForm) {
            replyForm.classList.toggle("d-none"); // Переключаем видимость формы

            // Если форма стала видимой, прокручиваем к ней
            if (!replyForm.classList.contains("d-none")) {
                setTimeout(() => {
                    replyForm.scrollIntoView({behavior: "smooth", block: "center"});
                }, 200);
            }
        }
    };

// Функция для отправки ответа
    window.submitReply = function (buttonElement) {
        const commentId = buttonElement.dataset.commentId;
        const articleId = buttonElement.dataset.articleId;
        const text = document.getElementById(`reply-text-${commentId}`).value.trim();

        if (!text) {
            alert("Комментарий не может быть пустым!");
            return;
        }

        fetch(`/article/${articleId}/comment/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({text: text, parent_id: commentId})
        })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Выводим данные для отладки
                if (data.success) {
                    let replyHtml = `
                    <div class="d-flex align-items-start mb-4 mt-2">
                        <div class="rounded-circle overflow-hidden" style="width: 40px; height: 40px;">
                            <img src="${data.avatar_url}" class="img-fluid" alt="${data.author}">
                        </div>
                        <div class="ms-3 flex-grow-1">
                            <div class="d-flex align-items-center mb-1">
                                <span class="badge badge-secondary fw-bold mb-0 me-2">${data.author}</span>
                                <p class="text-muted mb-0" style="font-size: 0.85rem;">
                                    <i class="fa-solid fa-calendar"></i> ${data.created_at}
                                </p>
                            </div>
                            <p class="mb-0">${data.text}</p>
                        </div>
                    </div>`;

                    document.getElementById(`replies-${commentId}`).innerHTML += replyHtml;
                    document.getElementById(`reply-text-${commentId}`).value = ""; // Очищаем поле ввода
                    document.getElementById(`reply-form-${commentId}`).classList.add("d-none"); // Скрываем форму
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error("Ошибка сети:", error));
    };
});

document.querySelectorAll('.like-btn, .dislike-btn').forEach(button => {
    button.addEventListener('click', function () {
        const commentId = this.getAttribute('data-comment-id');
        const isLike = this.classList.contains('like-btn');
        const action = isLike ? 'like' : 'dislike';

        fetch(`/vote-comment/${commentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: action })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            if (data.success) {
                const likeBtn = document.querySelector(`.like-btn[data-comment-id="${commentId}"]`);
                const dislikeBtn = document.querySelector(`.dislike-btn[data-comment-id="${commentId}"]`);

                // Обновляем счетчики
                likeBtn.querySelector('.count').textContent = data.likes;
                dislikeBtn.querySelector('.count').textContent = data.dislikes;

                // Сбрасываем классы активного состояния
                likeBtn.classList.remove('active');
                dislikeBtn.classList.remove('active');

                // Обновляем активный класс
                if (data.user_vote === 1) {
                    likeBtn.classList.add('active');
                } else if (data.user_vote === -1) {
                    dislikeBtn.classList.add('active');
                }
            }
        });
    });
});


// Функция для получения CSRF-токена
function getCsrfToken() {
    let tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenElement ? tokenElement.value : "";
}

document.addEventListener("DOMContentLoaded", function () {
    if (window.location.hash) {
        let target = document.querySelector(window.location.hash);
        if (target) {
            target.scrollIntoView({ behavior: "smooth", block: "center" });

            // Добавляем класс подсветки
            target.classList.add("highlight");

            // Убираем подсветку через 2 секунды
            setTimeout(() => target.classList.remove("highlight"), 2000);
        }
    }
});

