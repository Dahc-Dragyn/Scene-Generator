document.addEventListener("DOMContentLoaded", () => {
    const sceneInput = document.getElementById("scene-input");
    const generatePromptButton = document.getElementById("generate-prompt-button");
    const promptTextArea = document.getElementById("prompt-textarea");
    const generateImageButton = document.getElementById("generate-image-button");
    const imageDisplay = document.getElementById("image-display");
    const promptLoading = document.getElementById("prompt-loading");
    const imageLoading = document.getElementById("image-loading");

    // Function to show/hide loader and toggle button state
    const toggleLoading = (button, loader, show) => {
        if (show) {
            button.disabled = true;
            loader.style.display = 'block';
        } else {
            button.disabled = false;
            loader.style.display = 'none';
        }
    };

    generatePromptButton.addEventListener("click", async () => {
        const scene = sceneInput.value;
        console.log("Scene input:", scene);

        if (!scene.trim()) {
            alert("Please enter a scene description.");
            return;
        }

        toggleLoading(generatePromptButton, promptLoading, true);
        try {
            const response = await fetch("/generate-prompt", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ scene }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            promptTextArea.value = data.prompt;
        } catch (error) {
            console.error("Error generating prompt:", error);
            promptTextArea.value = `Failed to generate prompt: ${error.message}`;
        } finally {
            toggleLoading(generatePromptButton, promptLoading, false);
        }
    });

    generateImageButton.addEventListener("click", async () => {
        const prompt = promptTextArea.value;
        console.log("Prompt for image generation:", prompt);

        if (!prompt.trim()) {
            alert("Please enter or generate a prompt.");
            return;
        }

        toggleLoading(generateImageButton, imageLoading, true);
        try {
            const response = await fetch("/generate-image", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ prompt }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.image_path) {
                imageDisplay.src = data.image_path;
            } else {
                throw new Error(data.error || "Image generation failed.");
            }
        } catch (error) {
            console.error("Error generating image:", error);
            alert(error.message);
        } finally {
            toggleLoading(generateImageButton, imageLoading, false);
        }
    });
});