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

const backpack_button = document.querySelector('#backpack_button');
if (backpack_button) {
    backpack_button.addEventListener('click', function(evt){
    location.href = "intro.html";
});
}