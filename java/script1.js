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

async function win_screen() {
    const achievements_p = document.getElementById('achievements');
    const total_score_p = document.getElementById('total_score');

    const response = await fetch("http://127.0.0.1:3000/winning");
    const data = await response.json();

    const achievement_list = data.achievements
    const totalscore = data.score;
    const money = data.money;
    const time = data.time;
    const distance = data.total_distance;
    const moneyscore = data.money_score;
    const timescore = data.time_score;
    const distancescore = data.distance_score;
    const visited = data.visited_countries

    if (visited.length > 0) {

        total_score_p.textContent = "Along your journey you visited " + visited.join(", ") + " and travelled a total of " + distance + "km rewarding you "
            + distancescore + " points. You had a " + money + " dollars and " + time + " days left over rewarding you a " + moneyscore + " and "
            + timescore + " points each. Your total score was " + totalscore + " points. Congrulations!"
        } else {
        total_score_p.textContent = "Along your journey you travelled a total of " + distance + "km rewarding you "
            + distancescore + " points. You had a " + money + " dollars and " + time + " days left over rewarding you a " + moneyscore + " and "
            + timescore + " points each. Your total score was " + totalscore + " points. Congrulations!"
    }

    if (achievement_list.length > 0) {
        achievements_p.textContent = "You got the following achievements: " + achievement_list.join(", ");
    } else {
        achievements_p.textContent = "You got no achievements";
    }
}

win_screen()