async function scores() {

    const ul = document.createElement("ul");

    const response = await fetch("http://127.0.0.1:3000/scores");
    const data = await response.json();
    const scores = data.scores;

    const div = document.getElementById("scores_div");
    div.innerHTML = "";

    if (Object.entries(scores).length > 0) {

        for (let game in scores) {
            const li = document.createElement("li");
            li.textContent = `Game ${game}: ${scores[game]}`;
            ul.appendChild(li);
        }
    } else {
        const li = document.createElement("li");
        li.textContent = "No past scores!";
        ul.appendChild(li);
    }

    div.appendChild(ul);
}

scores();