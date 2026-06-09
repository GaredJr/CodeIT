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

const upvoteForms = document.querySelectorAll(".js-upvote-form");

upvoteForms.forEach((form) => {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const button = form.querySelector("button");
        if (!button || button.disabled) {
            return;
        }

        const previousText = button.innerText;
        button.disabled = true;
        button.innerText = "▲ ...";

        try {
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "X-Requested-With": "fetch",
                    "Accept": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("Upvote failed");
            }

            const data = await response.json();
            button.innerText = `▲ ${data.votes}`;
        } catch {
            button.innerText = previousText;
            form.submit();
            return;
        }

        button.disabled = false;
    });
});
