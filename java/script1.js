const instructions_button = document.querySelector('#instructions_button');
if (instructions_button) {
    instructions_button.addEventListener('click', function(evt){
    location.href = "instructions.html";
});
}

const scores_button = document.querySelector('#scores_button');
if (scores_button) {
    scores_button.addEventListener('click', function(evt){
    location.href = "scores.html";
});
}

const start_button = document.querySelector('#start_button');
if (start_button) {
    start_button.addEventListener('click', function(evt){
    location.href = "main.html";
});
}

const new_game_button = document.querySelector('#new_game_button');
if (new_game_button) {
    new_game_button.addEventListener('click', function(evt){
    location.href = "intro.html";
});
}

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