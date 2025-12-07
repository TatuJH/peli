let response;
let data;

async function scores() {

    const ul = document.createElement('ul');

    //Fetch scores from database via Flask
    response = await fetch('http://127.0.0.1:3000/scores');
    data = await response.json();

    const scorediv = document.getElementById('scores_div');
    scorediv.innerHTML = '';

    //Check if user has past scores recorded
    if (Object.entries(data.scores).length > 0) {

        //Make a new list object for each past score
        for (let i = 0; i < Object.entries(data.scores).length; i++) {
            const li = document.createElement('li');
            li.textContent = `Game ${i + 1}: ${data.scores[i + 1]}`;
            li.classList.add('score');
            ul.appendChild(li);
        }

    } else {

        //In case user has no past scores, create list object telling them this
        const li = document.createElement('li');
        li.textContent = 'No past scores.';
        ul.appendChild(li);

    }

    scorediv.appendChild(ul);
}

const play_again_button = document.getElementById('new_game_button');
play_again_button.addEventListener('click', () => {
   location.href='game.html';
});

const back_button = document.getElementById('back_button');
back_button.addEventListener('click', () => {
   location.href = 'index.html';
});

scores();
