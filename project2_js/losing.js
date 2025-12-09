let response;
let data;

async function lose_screen() {

    const losing_reason_p = document.getElementById('losing_reason');
    const location_li = document.getElementById('location')
    const visited_li = document.getElementById('visited');
    const leftovers_li = document.getElementById('leftovers');
    const artefacts_li = document.getElementById('artefacts')

    response = await fetch('http://127.0.0.1:3000/lose_screen');
    data = await response.json();

    losing_reason_p.textContent = "Unfortunately, you hava lost. But don't worry! You can still play again anytime you want :)!"

    location_li.textContent = "Your journey ended in " + data.airport + " in " + data.country + ", " + data.cont + ".";
    visited_li.textContent = "Along your journey you visited " + data.visited_countries.join(", ") + "and travelled a total of " + data.total_distance + "km.";
    leftovers_li.textContent = "You had " + data.money + " dollars and " + data.time + " days.";

    if (data.artefacts.length > 0) {
        artefacts_li.textContent = "You owned the following artefacts: " + data.artefacts.join(", ") + ".";
    } else {
        artefacts_li.textContent = "You didn't have any artefacts.";
    }
}

const play_again_button = document.getElementById('new_game_button');
play_again_button.addEventListener('click', async() => {
    await fetch('http://127.0.0.1:3000/reset', { method: 'POST' });
   location.href='../project2_htm/game.html';
});

const main_menu_button = document.getElementById('main_menu_button');
main_menu_button.addEventListener('click', () => {
   location.href='../project2_htm/index.html';
});

lose_screen()