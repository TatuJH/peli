const play_again_button = document.getElementById('new_game_button');
play_again_button.addEventListener('click', async() => {
    await fetch('http://127.0.0.1:3000/reset', { method: 'POST' });
   location.href='game.project2_htm';
});

const back_button = document.getElementById('back_button');
back_button.addEventListener('click', () => {
   location.href = 'index.project2_htm';
});
