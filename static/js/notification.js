document.addEventListener("DOMContentLoaded", function () {
    const bell = document.getElementById("navbarDropdownMenuLink");
    const dropdown = document.getElementById("notification-dropdown");
    const notificationList = document.getElementById("notification-list");
    const clearButton = document.getElementById("clear-notifications");
    const badge = document.getElementById("notification-badge");

    // Функция загрузки уведомлений
    function loadNotifications() {
        fetch("/notifications/")
            .then((response) => response.json())
            .then((data) => {
                notificationList.innerHTML = ""; // Очищаем список
                if (data.notifications.length === 0) {
                    notificationList.innerHTML = "<p class='dropdown-item text-muted'>Нет новых уведомлений</p>";
                } else {
                    data.notifications.forEach((notif) => {
                        let item = document.createElement("li");
                        let link = document.createElement("a");
                        link.href = notif.url;
                        link.classList.add("dropdown-item");
                        link.innerText = notif.text;
                        link.addEventListener("click", function (e) {
                            e.preventDefault();
                            markNotificationAsRead(notif.id, notif.url);
                        });
                        item.appendChild(link);
                        notificationList.appendChild(item);
                    });
                }
                badge.textContent = data.notifications.length;
                badge.style.display = data.notifications.length > 0 ? "inline" : "none";
            });
    }

    // Функция пометки одного уведомления как прочитанного
    function markNotificationAsRead(id, url) {
        fetch(`/notifications/read/${id}/`, {
            method: "POST", headers: {
                'X-CSRFToken': getCsrfToken()
            },
        })
            .then(() => {
                window.location.href = url; // Переход по ссылке после пометки
            });
    }

    // Функция очистки всех уведомлений
    clearButton.addEventListener("click", function () {
        fetch("/notifications/read-all/", {
            method: "POST", headers: {
                'X-CSRFToken': getCsrfToken()
            },
        })
            .then(() => {
                notificationList.innerHTML = "<p class='dropdown-item text-muted'>Нет новых уведомлений</p>";
                badge.style.display = "none";
            });
    });

    // Открытие dropdown при клике на колокольчик
    bell.addEventListener("click", function () {
        loadNotifications();
    });

    // Загружаем уведомления при загрузке страницы
    loadNotifications();
});

function getCsrfToken() {
    let tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenElement ? tokenElement.value : "";
}