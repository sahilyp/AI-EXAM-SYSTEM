let design = 1;

function toggleTheme() {
    document.body.classList.toggle("dark");
    document.body.classList.toggle("light");
}

function toggleDesign() {
    const box = document.querySelector(".container");
    design = design === 1 ? 2 : 1;
    box.className = "container design" + design;
}

function generateMCQ() {
    const text = document.getElementById("text").value;
    const count = document.getElementById("count").value;
    const difficulty = document.getElementById("difficulty").value;
    const loader = document.getElementById("loader");
    const container = document.getElementById("mcq-container");

    if (!text) {
        alert("Enter some text");
        return;
    }

    container.innerHTML = "";
    loader.classList.remove("hidden");

    fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text, count, difficulty })
    })
    .then(res => res.json())
    .then(data => {
        loader.classList.add("hidden");

        data.questions.forEach((q, i) => {
            let card = document.createElement("div");
            card.className = "mcq-card";

            card.innerHTML = `
                <h3>Q${i+1}. ${q.question}</h3>
                ${q.options.map(o =>
                    `<div class="option" onclick="check(this,'${o}','${q.answer}','${q.explanation}')">${o}</div>`
                ).join("")}
                <div class="explanation hidden"></div>
            `;
            container.appendChild(card);
        });
    });
}

function check(el, selected, correct, explanation) {
    const options = el.parentElement.querySelectorAll(".option");
    const exp = el.parentElement.querySelector(".explanation");

    options.forEach(o => o.onclick = null);

    if (selected === correct) {
        el.classList.add("correct");
        exp.innerHTML = "✅ Correct<br>" + explanation;
    } else {
        el.classList.add("wrong");
        exp.innerHTML = "❌ Wrong<br><b>Correct:</b> " + correct + "<br>" + explanation;
    }

    exp.classList.remove("hidden");
}
