const copyButtons = document.querySelectorAll(".code-header button");

copyButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const codeBlock = button.closest(".code-preview").querySelector("code");
        if (!codeBlock) {
            return;
        }

        const previousText = button.innerText;
        const code = codeBlock.innerText;

        try {
            await navigator.clipboard.writeText(code);
            button.innerText = "Copied";
        } catch {
            button.innerText = "Failed";
        }

        setTimeout(() => {
            button.innerText = previousText;
        }, 1200);
    });
});
