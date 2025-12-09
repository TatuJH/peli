let response;
let data;

async function win_screen() {

    const achievements_p = document.getElementById('achievements');
    const total_score_p = document.getElementById('total_score');

    response = await fetch('http://127.0.0.1:3000/win_screen');
    data = await response.json();

    total_score_p.textContent = 'Along your journey you visited ' + data.visited_countries.join(', ') + ' and travelled a total of ' + data.total_distance + 'km rewarding you '
        + data.distance_score + ' points. You had a ' + data.money + ' dollars and ' + data.time + ' days left over rewarding you a ' + data.money_score + ' and '
        + data.time_score + ' points respectively. Your total score was ' + data.score + ' points. Congratulations!'

    if (data.achievements.length > 0) {
        achievements_p.textContent = 'You got the following achievements: ' + data.achievements.join(', ');
    } else {
        achievements_p.textContent = 'You got no achievements';
    }
}

const play_again_button = document.getElementById('new_game_button');
play_again_button.addEventListener('click', () => {
   location.href='../project2_htm/game.html';
});

const main_menu_button = document.getElementById('main_menu_button');
main_menu_button.addEventListener('click', () => {
   location.href='../project2_htm/index.html';
});

win_screen()