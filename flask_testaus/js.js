let response = "";
let data = "";
//
// const eventText = document.getElementById('eventText');
//
// const stats = document.getElementById('stats');
//
// // const buttons = document.getElementsByClassName('button');
// //
// // // for (let button of buttons) {
// // //     button.addEventListener('click', (evt) => {
// // //         evt.preventDefault()
// // //         a(button.name, button.value);
// // //     });
// // // }
// // //
// // //
// // // async function a(action, number) {
// // // //     if (action === "event") {
// // // //         response = await fetch(`http://127.0.0.1:3000/${action}/${number}`);
// // // //         data = await response.json();
// // // //         update(data)
// // // //     }
// // // //     else if (action === "scores") {
// // // //         response = await fetch(`http://127.0.0.1:3000/${action}`);
// // // //         data = await response.json();
// // // //         update(data)
// // // //     }
// // // //     else if (action === "intro_text") {
// // // //         response = await fetch(`http://127.0.0.1:3000/${action}`);
// // // //         data = await response.json();
// // // //         update(data)
// // // //     }
// // // // }
// //
// // function update(info) {
// //     eventText.textContent = info['text'];
// //     stats.textContent = 'Money: ' + info['money'];
// // }

const div = document.getElementById("div");
const eventdiv = document.createElement('div');
eventdiv.id = "eventdiv";
div.appendChild(eventdiv);
const stats = document.getElementById("stats");
const geteventbtn = document.createElement("button");
geteventbtn.classList.add('button');
geteventbtn.id = 'event';
geteventbtn.textContent = 'EVENT';

eventdiv.appendChild(geteventbtn);

const eventbtn = document.getElementById("event");

eventbtn.addEventListener('click', async function(evt) {
    evt.preventDefault();

    div.innerHTML = '';
    div.appendChild(eventdiv);

    eventdiv.innerHTML = '';

    response = await fetch('http://127.0.0.1:3000/events/get/0/x');
    data = await response.json();

    const text = document.createElement('p');
    text.textContent = data['text'];
    eventdiv.appendChild(text);

    const question = document.createElement('p');
    question.textContent = data['question'];
    eventdiv.appendChild(question);

    for (let i = 0; i < data['choices'].length; i++) {
        const eventbutton = document.createElement('button');
        eventbutton.textContent = data['choices'][i];
        eventbutton.value = data['choices'][i];
        eventbutton.classList.add('button');
        eventbutton.setAttribute('money', data['money_costs'][i]);
        eventbutton.setAttribute('time', data['time_costs'][i]);
        eventbutton.setAttribute('artefacts', data['artefacts_costs'][i]);
        eventbutton.addEventListener('click', async function(evt) {
            evt.preventDefault();
            if (data['money'] >= eventbutton.getAttribute('money') && data['time'] >= eventbutton.getAttribute('time')) {
            eventdiv.innerHTML = '';

            response = await fetch(`http://127.0.0.1:3000/events/result/${data['number']}/${eventbutton.value}`);
            data = await response.json();

            const text = document.createElement('p');
            text.textContent = data['text'];
            eventdiv.appendChild(text);

            stats.textContent = `Money: ${data['money']}, time: ${data['time']}`;

            eventdiv.appendChild(eventbtn);
            } else {
                const error = document.createElement('p');
                error.textContent = 'Not enough resources';
                eventdiv.appendChild(error);
            }
        })
        eventdiv.appendChild(eventbutton);
    }
});

const fightdiv = document.createElement('div');
fightdiv.id="fightdiv";
div.appendChild(fightdiv);
const getfightbutton = document.createElement("button");
getfightbutton.classList.add('button');
getfightbutton.id = 'fight';
getfightbutton.textContent = 'FIGHT';

fightdiv.appendChild(getfightbutton);

const fightbtn = document.getElementById('fight');

fightbtn.addEventListener('click', async function(evt) {
    evt.preventDefault();

    div.innerHTML = '';
    div.appendChild(fightdiv);

    fightdiv.innerHTML = '';

    response = await fetch('http://127.0.0.1:3000/fight/start/9');
    data = await response.json();

    const player = document.createElement('p');
    player.id="player";
    player.innerHTML = `HP: <span class="hp-text">${data["player_hp"]}</span>, remaining heals: <span class="ptn-text">${data["player_heals"]}</span>`;
    fightdiv.appendChild(player);

    const text = document.createElement('p');
    text.id="fighttxt";
    text.textContent = data['text'];
    fightdiv.appendChild(text);


    for (let i = 0; i < Object.keys(data['enemies_in_fight']).length; i++) {
        const enemy = document.createElement('p');
        enemy.id=`fightenemy${i}`
        enemy.innerHTML = `Enemy ${i + 1}: ${data['enemies_in_fight'][i.toString()]['type']} <span class="hp-text">${data['enemies_in_fight'][i.toString()]['hp']}</span> <span class="spd-text">(charging for ${data['enemies_in_fight'][i.toString()]['spd']} turns)</span>`;
        fightdiv.appendChild(enemy);
    }

    for (let i = 0; i < Object.keys(data['enemies_in_fight']).length; i++) {
        const fight = document.createElement('button');
        fight.textContent = `Strike enemy ${i + 1} (${data['enemies_in_fight'][i.toString()]['type']})`
        fight.value = i.toString();
        fight.classList.add('button');

        fight.addEventListener('click', async function(evt) {
            evt.preventDefault();

            response = await fetch(`http://127.0.0.1:3000/fight/strike/${fight.value}`);
            data = await response.json();

            document.getElementById('fighttxt').textContent = data['text'];

            for (let i = 0; i < Object.keys(data['enemies_in_fight']).length; i++) {
                if (data['enemies_in_fight'][i]['hp'] > 0) {
                    document.getElementById(`fightenemy${i}`).innerHTML = `Enemy ${i + 1}: ${data['enemies_in_fight'][i.toString()]['type']} <span class="hp-text">${data['enemies_in_fight'][i.toString()]['hp']}</span> <span class="spd-text">(charging for ${data['enemies_in_fight'][i.toString()]['spd']} turns)</span>`;
                }
            }
            document.getElementById('player').innerHTML = `HP: <span class="hp-text">${data["player_hp"]}</span>, remaining heals: <span class="ptn-text">${data["player_heals"]}</span>`;
            if (data['enemies_in_fight'][fight.value]['hp'] <= 0) {
                fightdiv.removeChild(document.getElementById(`fightenemy${fight.value}`));
                fightdiv.removeChild(fight);
            }
            if (data['player_hp'] <= 0) {
                fightdiv.innerHTML = '';
            }
            if (data['amount'] <= 0) {
                fightdiv.innerHTML = '';
            }
        })
        fightdiv.appendChild(fight);
    }

    if (data['player_heals'] > 0) {
        const heal = document.createElement('button');
        heal.textContent = 'Heal';
        heal.classList.add('button');

        heal.addEventListener('click', async function(evt) {
            evt.preventDefault();

            response = await fetch(`http://127.0.0.1:3000/fight/heal/9`);
            data = await response.json();

            document.getElementById('fighttxt').textContent = data['text'];

            document.getElementById('player').innerHTML = `HP: <span class="hp-text">${data["player_hp"]}</span>, remaining heals: <span class="ptn-text">${data["player_heals"]}</span>`;
            for (let i = 0; i < Object.keys(data['enemies_in_fight']).length; i++) {
                    if (data['enemies_in_fight'][i]['hp'] > 0) {
                        document.getElementById(`fightenemy${i}`).innerHTML = `Enemy ${i + 1}: ${data['enemies_in_fight'][i.toString()]['type']} <span class="hp-text">${data['enemies_in_fight'][i.toString()]['hp']}</span> <span class="spd-text">(charging for ${data['enemies_in_fight'][i.toString()]['spd']} turns)</span>`;
                    }
                }

            if (data['player_heals'] <= 0) {
                fightdiv.removeChild(heal);
            }
        })
        fightdiv.appendChild(heal);
    }

    const guard = document.createElement('button');
    guard.textContent = 'Guard';
    guard.classList.add('button');
    guard.addEventListener('click', async function(evt) {
        evt.preventDefault();

        response = await fetch(`http://127.0.0.1:3000/fight/guard/9`);
        data = await response.json();

        document.getElementById('fighttxt').textContent = data['text'];

        document.getElementById('player').innerHTML = `HP: <span class="hp-text">${data["player_hp"]}</span>, remaining heals: <span class="ptn-text">${data["player_heals"]}</span>`;
            for (let i = 0; i < Object.keys(data['enemies_in_fight']).length; i++) {
                    if (data['enemies_in_fight'][i]['hp'] > 0) {
                        document.getElementById(`fightenemy${i}`).innerHTML = `Enemy ${i + 1}: ${data['enemies_in_fight'][i.toString()]['type']} <span class="hp-text">${data['enemies_in_fight'][i.toString()]['hp']}</span> <span class="spd-text">(charging for ${data['enemies_in_fight'][i.toString()]['spd']} turns)</span>`;
                    }
                }
    })
    fightdiv.appendChild(guard);
})