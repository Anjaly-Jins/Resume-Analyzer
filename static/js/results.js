document.addEventListener("DOMContentLoaded", () => {

    // Animate the score counting up
    const scoreElement = document.getElementById("score");

    if (scoreElement) {

        const finalScore = parseFloat(scoreElement.innerText);

        let current = 0;

        const interval = setInterval(() => {

            current += 1;

            if (current >= finalScore) {

                current = finalScore;

                clearInterval(interval);

            }

            scoreElement.innerText = current.toFixed(0);

        }, 20);

    }

    // Hover effect for cards
    const cards = document.querySelectorAll(".glass, .stat-card, .score-card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {
            card.style.transform = "translateY(-8px)";
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "translateY(0)";
        });

    });

});