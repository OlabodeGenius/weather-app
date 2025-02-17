document.addEventListener("DOMContentLoaded", () => {
    const weatherDescription = document.querySelector(".description");
    const animationContainer = document.getElementById("weather-animation");

    if (weatherDescription) {
        const description = weatherDescription.textContent.toLowerCase();

        // Clear previous animations
        animationContainer.innerHTML = "";

        // Add animations based on weather condition
        if (description.includes("snow")) {
            createSnowEffect(animationContainer);
        } else if (description.includes("rain")) {
            createRainEffect(animationContainer);
        } else if (description.includes("clear")) {
            createSunEffect(animationContainer);
        } else if (description.includes("wind")) {
            createWindEffect(animationContainer);
        }
    }
});

function createSnowEffect(container) {
    for (let i = 0; i < 50; i++) {
        const snowflake = document.createElement("div");
        snowflake.classList.add("snowflake");
        snowflake.style.left = `${Math.random() * 100}%`;
        snowflake.style.animationDuration = `${Math.random() * 3 + 2}s`;
        container.appendChild(snowflake);
    }
}

function createRainEffect(container) {
    for (let i = 0; i < 50; i++) {
        const raindrop = document.createElement("div");
        raindrop.classList.add("raindrop");
        raindrop.style.left = `${Math.random() * 100}%`;
        raindrop.style.animationDuration = `${Math.random() * 0.5 + 0.2}s`;
        container.appendChild(raindrop);
    }
}

function createSunEffect(container) {
    container.style.background = "linear-gradient(to bottom, #ffeb3b, #fff3e0)";
}

function createWindEffect(container) {
    container.style.background = "linear-gradient(to right, #e0f7fa, #b3e5fc)";
    const windLine = document.createElement("div");
    windLine.style.position = "absolute";
    windLine.style.width = "100%";
    windLine.style.height = "2px";
    windLine.style.background = "#81d4fa";
    windLine.style.top = "50%";
    windLine.style.animation = "wind 2s linear infinite";
    container.appendChild(windLine);
}

// Wind Animation
const windKeyframes = `
@keyframes wind {
    0% {
        transform: translateX(-100%);
    }
    100% {
        transform: translateX(100%);
    }
}`;
const styleSheet = document.createElement("style");
styleSheet.innerHTML = windKeyframes;
document.head.appendChild(styleSheet);