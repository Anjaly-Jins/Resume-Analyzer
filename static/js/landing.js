document.addEventListener("DOMContentLoaded", () => {

    const hero = document.querySelector(".hero");
    const title = document.querySelector(".hero h1");
    const text = document.querySelector(".hero p");
    const button = document.querySelector("button");

    hero.style.opacity = "1";

    title.classList.add("show");

    setTimeout(() => {
        text.classList.add("show");
    }, 300);

    setTimeout(() => {
        button.classList.add("show");
    }, 600);

});