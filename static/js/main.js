const copyButtons = document.querySelectorAll(".code-header button");

copyButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const codeBlock = button.closest(".code-preview").querySelector("code");
        const code = codeBlock.innerText;

        await navigator.clipboard.writeText(code);

        button.innerText = "Copied";

        setTimeout(() => {
            button.innerText = "Copy";
        }, 1200);
    });
});