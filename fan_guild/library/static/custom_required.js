// Данный скрипт только добавляет красные звездочки к обязательным полям
// Ибо штатная Django статика этого не умеет.
// Данный скрипт подключается в templates/change_form.html

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll("label.required").forEach(function (label) {
        if (!label.querySelector(".req-star")) {
            const star = document.createElement("span");
            star.className = "req-star";
            star.textContent = " *";
            star.style.color = "red";
            star.style.fontWeight = "bold";
            label.appendChild(star);
        }
    });
});

document.addEventListener("formset:added", function () {
    restoreForm();
});