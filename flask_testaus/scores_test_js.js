async function scores() {

    if (scores.length > 0) {

        const div = document.getElementById("scores");
        div.innerHTML = "";

        const response = await fetch("http://127.0.0.1:3000/scores");
        const data = await response.json();
        const scores = data.scores;

        const ul = document.createElement("ul");

        for (let game in scores) {
            const li = document.createElement("li");
            li.textContent = `Game ${game}: ${scores[game]}`;
            ul.appendChild(li);
        }
    }

    else if (scores.length === 0) {
        const li = document.createElement("li");
        li.textContent = "No past scores!";
        ul.appendChild(li);
    }

    div.appendChild(ul);
}

scores();