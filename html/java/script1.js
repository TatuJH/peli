const instructions = document.querySelector('#instructions');
if (instructions) {
    instructions.addEventListener('click', function(evt){
    location.href = "instructions.html";
});
}

const scores = document.querySelector('#scores');
if (scores) {
    scores.addEventListener('click', function(evt){
    location.href = "scores.html";
});
}

const start = document.querySelector('#start');
if (start) {
    start.addEventListener('click', function(evt){
    location.href = "main.html";
});
}

const new_game = document.querySelector('#new_game');
if (new_game) {
    new_game.addEventListener('click', function(evt){
    location.href = "intro.html";
});
}