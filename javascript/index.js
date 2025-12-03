//Initialize main menu buttons
const instructions_button = document.querySelector('#instructions_button');
instructions_button.addEventListener('click', () => {
    location.href = 'intro.html';
});
const scores_button = document.querySelector('#scores_button');
scores_button.addEventListener('click', () => {
    location.href = 'scores.html';
});
const start_button = document.querySelector('#start_button');
start_button.addEventListener('click', () => {
    location.href = 'game.html';
});