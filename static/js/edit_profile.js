document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("edit-profile-btn");
    const cancelBtn = document.getElementById("cancel-edit-btn");
    const profileInfo = document.getElementById("profile-info");
    const editForm = document.getElementById("profile-edit-form");

    editBtn.addEventListener("click", function () {
        profileInfo.classList.add("d-none");
        editForm.classList.remove("d-none");
    });

    cancelBtn.addEventListener("click", function () {
        editForm.classList.add("d-none");
        profileInfo.classList.remove("d-none");
    });
});