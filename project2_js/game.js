//-------------- Variables --------------

let response;
let data;
let sub_data;           // Just in case

let map = null;
let departHandler = null;
let shopping = false;

//-------------- Permanent Elements --------------

const main_div          = document.getElementById("main");
const left_div          = document.getElementById('left_div');
const right_div         = document.getElementById('right_div');
const event_div         = document.getElementById('event_div');
const fight_div         = document.getElementById('fight_div');
const work_div          = document.getElementById('work_div');
const map_container     = document.getElementById('map_container');
const map_div           = document.getElementById('map_div');
const map_text          = document.getElementById('map_text');
const airport_info      = document.getElementById('airport_text');
const shop_div          = document.getElementById('shop_div');
const inv_div           = document.getElementById('inventory_div');
const achievement_div   = document.getElementById('achievement_div');

const action_buttons    = document.getElementById('action_buttons');
const main_buttons      = document.getElementById('main_buttons');
const work_button       = document.getElementById('work_button');
const event_button      = document.getElementById('event_button');
const fight_button      = document.getElementById('fight_button');
const shop_button       = document.getElementById("shop_button");
const map_button        = document.getElementById('map_button');
const inv_button        = document.getElementById('inv_button');
const return_button     = document.getElementById("return_button");
const depart_button     = document.getElementById('depart_button');

const money_display     = document.getElementById('money_display');
const time_display      = document.getElementById('time_display');
const actions_display   = document.getElementById('actions_display');
const artefact_display  = document.getElementById("artefacts_display");
const co2_display       = document.getElementById('co2_display');
const popup             = document.getElementById('popup');

const inv_list          = document.getElementsByClassName("art");

//-------------- Helper Functions --------------

function hideAll() {
    right_div.querySelectorAll('div').forEach(child => child.classList.add('hidden'));
    left_div.querySelectorAll('div').forEach(child => child.classList.add('hidden'));

    left_div.className = '';
    left_div.classList.add('split_screen');

    hide(return_button);

    fight_div.querySelectorAll('p').forEach(child => child.remove());
}

function removeActions() {
    action_buttons.querySelectorAll('button').forEach(child => {
        if (!child.classList.contains('return_button') &&
            child.id !== "return_button" &&
            child.id !== "depart_button") {
            child.remove();
        }
    });
}

function hide(thing)  { thing.classList.add('hidden'); }
function show(thing)  { thing.classList.remove('hidden'); }

hide(popup);

function popupfunc(text) {
    show(popup);
    popup.textContent = text;
    setTimeout(() => hide(popup), 3000);
}

//-------------- Stats & Inventory --------------

async function updateStats() {
    money_display.textContent    = `Money: ${data.game_state.money}`;
    time_display.textContent     = `Time: ${data.game_state.time}`;
    actions_display.textContent  = `Actions left: ${data.game_state.actions}`;
    co2_display.textContent      = `CO₂: ${data.game_state.co2}`;
    artefact_display.textContent = data.game_state.artefact_display;

    if (data.game_state.artefacts > 0) {
        const arts = JSON.parse(data.game_state.all_artefacts);

        for (let i = 0; i < inv_list.length; i++) {
            if (arts[i]) {
                const button = inv_list[i];
                button.textContent = `Artefact name: ${arts[i]["name"]} \nValue: $${arts[i]["value"]}\nContinent: ${arts[i]["continent"]}`;

                button.addEventListener("click", async function handler() {
                    response = await fetch(`http://127.0.0.1:3000/shop/sell/${i}`);
                    data = await response.json();

                    money_display.textContent = `Money: ${data.game_state.money}`;
                    button.textContent = "Myyty!";
                    button.removeEventListener("click", handler);
                }, { once: true });

                button.disabled = !shopping;
            } else {
                inv_list[i].textContent = "backpack slot :p";
            }
        }
    }

    achievements();

    if (data.game_state.time <= 0 || data.game_state.actions < 0) {
        location.href = '../project2_htm/lose_screen.html';
    }
}

//-------------- Map & Departure --------------

async function depart() {
    hideAll();

    return_button.textContent = 'Return';
    show(map_container);
    show(map_div);
    show(map_text);
    show(return_button);

    if (map) map.remove();

    map = L.map('map_div', {
        worldCopyJump: false,
        minZoom: 2,
        maxZoom: 20
    }).setView([0, 0], 2);

    map.setMaxBounds([-90, -180], [90, 180]);
    map.on('drag', () => map.panInsideBounds([[-90, -180], [90, 180]], { animate: false }));

    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}').addTo(map);

    response = await fetch('http://127.0.0.1:3000/airport/get/0/0/0/0/0/0');
    data = await response.json();
    updateStats();

    const maptext = document.createElement('p');
    maptext.textContent = "Select airport. The darker the blue, the larger the airport.";
    map_text.appendChild(maptext);

    for (let i = 0; i < data.info[0].length; i++) {
        let color;
        if (i === 0) color = "red";
        else if (i === 1 && data.info[0].length !== 19) color = '#7CFC00';
        else if (data.info[0][i].type === "large_airport")   color = "navy";
        else if (data.info[0][i].type === "medium_airport")  color = "dodgerblue";
        else if (data.info[0][i].type === "small_airport")   color = "lightskyblue";

        const circle = L.circleMarker(
            [data.info[0][i].latitude, data.info[0][i].longitude],
            { opacity: 0, fillColor: color, fillOpacity: 1, radius: 20 }
        ).addTo(map);

        if (i !== 0) {
            circle.addEventListener('click', () => {
                airport_info.innerHTML = `${data.info[0][i].aname}, ${data.info[0][i].cname} (${data.info[0][i].alt_cont}), <span class="moneytext">$${data.info[0][i].cost}</span>, ${data.info[0][i].distance}km, ${data.info[0][i].co2} CO₂<br><br>Thus far you have travelled ${data.game_state.distance}km.`;
                show(airport_info);

                const departHandler = async function() {
                    if (data.game_state.money >= data.info[0][i].cost) {
                        if (i === 1 && data.info[0].length !== 19 && data.game_state.unique_artefacts === 6) {
                            await fetch(`http://127.0.0.1:3000/win_screen`);
                        }

                        response = await fetch(`http://127.0.0.1:3000/airport/depart/${data.info[0][i].aname}/${data.info[0][i].cname}/${data.info[0][i].type}/${data.info[0][i].cost}/${data.info[0][i].continent}/${i}`);
                        data = await response.json();
                        updateStats();

                        map_text.removeChild(maptext);
                        depart_button.removeEventListener('click', departHandler);
                        depart_button.removeEventListener('mouseover', departHover);
                        depart_button.removeEventListener('mouseout', departOut);
                        removeActions();
                        hideAll();
                        hide(return_button);
                        hide(depart_button);
                        show(main_buttons);
                    } else {
                        if (data.game_state.money < data.info[0][i].cost && data.game_state.actions === 0) {
                            location.href = '../project2_htm/lose_screen.html';
                        } else {
                            popupfunc("Not enough money to fly!");
                        }
                    }
                };

                const departHover = () => {};
                const departOut   = () => {};

                depart_button.addEventListener('click', departHandler, { once: true });
                depart_button.addEventListener('mouseover', departHover);
                depart_button.addEventListener('mouseout', departOut);

                show(return_button);
                show(depart_button);

                return_button.addEventListener('click', () => hide(depart_button), { once: true });
            });

            circle.on('mouseover', () => {
                circle.setStyle({ fillOpacity: 0.5 });
                maptext.innerHTML = `${data.info[0][i].aname}, ${data.info[0][i].cname} (${data.info[0][i].alt_cont}), <span class='moneytext'>$${data.info[0][i].cost}</span>, ${data.info[0][i].distance}km, ${data.info[0][i].co2} CO₂`;
            });
            circle.on('mouseout', () => {
                circle.setStyle({ fillOpacity: 1 });
                maptext.textContent = "Select airport. The darker the blue, the larger the airport.";
            });
        } else {
            circle.on('mouseover', () => {
                circle.setStyle({ fillOpacity: 0.5 });
                maptext.textContent = `You are currently in ${data.info[0][i].aname}, ${data.info[0][i].cname} (${data.info[0][i].alt_cont})`;
            });
            circle.on('mouseout', () => {
                circle.setStyle({ fillOpacity: 1 });
                maptext.textContent = "Select airport. The darker the blue, the larger the airport.";
            });
        }
    }

    show(action_buttons);
}

//-------------- Achievements --------------

const seenAchievements = {};

async function achievements() {
    const achievements_list = document.getElementById('achievement_list');

    response = await fetch('http://127.0.0.1:3000/ach');
    sub_data = await response.json();

    for (let i = 0; i < sub_data.info[0].length; i++) {
        const ach = sub_data.info[0][i];
        const li = document.createElement('li');
        li.textContent = ach.name;
        li.className = "ach";
        achievements_list.appendChild(li);

        li.addEventListener('mouseover', () => li.textContent = ach.description);
        li.addEventListener('mouseout',  () => li.textContent = ach.name);

        if (seenAchievements[ach.name] !== true) {
            seenAchievements[ach.name] = true;

            (function(achievement, delay) {
                setTimeout(() => {
                    show(popup);
                    if (achievement.category === "distance") {
                        popup.textContent =  `Enviroment Tax: ${achievement.name} for $${achievement.reward}!`;
                        } else {
                        popup.textContent = `New achievement: ${achievement.name} for $${achievement.reward}!`;
                        }

                    setTimeout(() => hide(popup), 4000);
                }, delay);
            })(ach, i * 4300);
        }
    }
}

//-------------- Permanent Event Listeners --------------

map_button.addEventListener('click', depart);

event_button.addEventListener('click', async () => {
    hideAll();
    hide(return_button);

    response = await fetch('http://127.0.0.1:3000/events/get/0/x');
    data = await response.json();

    const event_text = document.createElement('p');
    event_text.innerHTML = `${data.info[0].text}<br><br>${data.info[0].question}`;
    event_div.appendChild(event_text);

    for (let i = 0; i < data.info[0].choices.length; i++) {
        const choice_button = document.createElement('button');
        choice_button.textContent = data.info[0].choices[i];
        choice_button.classList.add('button');

        choice_button.addEventListener('click', async () => {
            if (data.game_state.money >= data.info[0].money_costs[i] &&
                data.game_state.time  >= data.info[0].time_costs[i] &&
                data.game_state.artefacts >= data.info[0].artefacts_costs[i]) {

                response = await fetch(`http://127.0.0.1:3000/events/result/${data.info[0].number}/${data.info[0].choices[i]}`);
                data = await response.json();
                updateStats();
                removeActions();

                event_text.innerHTML = data.info[0].text;

                return_button.textContent = "OK";
                show(return_button);
                return_button.addEventListener('click', () => {
                    event_text.remove();
                    hideAll();
                    show(main_buttons);
                }, { once: true });
            } else {
                popupfunc("Not enough resources!");
            }
        });

        action_buttons.appendChild(choice_button);
    }

    show(action_buttons);
    show(event_div);
});

fight_button.addEventListener('click', async () => {
    const updateFight = () => {
        fight_text.innerHTML = `${data.info[0].text}<br><br>HP: <span class="hp-text">${data.info[0].player_hp}</span>, remaining heals: <span class="ptn-text">${data.info[0].player_heals}</span><br>`;

        for (let i = 0; i < Object.keys(data.info[0].enemies_in_fight).length; i++) {
            if (data.info[0].enemies_in_fight[i].hp > 0) {
                fight_text.innerHTML += `<br>Enemy ${i + 1}: ${data.info[0].enemies_in_fight[i].type} <span class="hp-text">${data.info[0].enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.info[0].enemies_in_fight[i].spd} turns)</span>`;
            }
        }

        if (data.info[0].player_hp <= 0) {
            removeActions();
            fight_div.querySelectorAll('p').forEach(p => p.remove());

            return_button.textContent = "OK";
            show(return_button);
            fight_text.innerHTML = "One of the heretics knocks you out for <span class='timetext'>10 days</span>.";
            fight_div.appendChild(fight_text);
            updateStats();
        }

        if (data.info[0].amount <= 0) {
            removeActions();
            fight_div.querySelectorAll('p').forEach(p => p.remove());

            return_button.textContent = "OK";
            show(return_button);
            fight_text.innerHTML = `You convert all the heretics. Your god is pleased and blesses you with <span class='moneytext'>$${data.info[0].money_get}</span>.`;
            fight_div.appendChild(fight_text);
            updateStats();
        }
    };

    hideAll();
    hide(return_button);

    response = await fetch('http://127.0.0.1:3000/fight/start/0');
    data = await response.json();
    updateStats();

    const fight_text = document.createElement('p');
    fight_text.innerHTML = `${data.info[0].text}<br><br>HP: <span class="hp-text">${data.info[0].player_hp}</span>, remaining heals: <span class="ptn-text">${data.info[0].player_heals}</span><br>`;
    for (let i = 0; i < Object.keys(data.info[0].enemies_in_fight).length; i++) {
        fight_text.innerHTML += `<br>Enemy ${i + 1}: ${data.info[0].enemies_in_fight[i].type} <span class="hp-text">${data.info[0].enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.info[0].enemies_in_fight[i].spd} turns)</span>`;
    }
    fight_div.appendChild(fight_text);

    for (let i = 0; i < Object.keys(data.info[0].enemies_in_fight).length; i++) {
        const strike_button = document.createElement('button');
        strike_button.textContent = `Strike enemy ${i + 1} (${data.info[0].enemies_in_fight[i].type})`;
        strike_button.classList.add('button', 'attack');
        action_buttons.appendChild(strike_button);

        strike_button.addEventListener('click', async () => {
            response = await fetch(`http://127.0.0.1:3000/fight/strike/${i}`);
            data = await response.json();
            updateStats();
            updateFight();

            if (data.info[0].enemies_in_fight[i].hp <= 0) {
                action_buttons.removeChild(strike_button);
            }
        });
    }

    if (data.info[0].player_heals > 0) {
        const heal_button = document.createElement('button');
        heal_button.textContent = 'Heal';
        heal_button.classList.add('button', 'nonattack');
        heal_button.addEventListener('click', async () => {
            response = await fetch(`http://127.0.0.1:3000/fight/heal/0`);
            data = await response.json();
            updateStats();
            updateFight();

            if (data.info[0].player_heals <= 0) {
                action_buttons.removeChild(heal_button);
            }
        });
        action_buttons.appendChild(heal_button);
    }

    const guard_button = document.createElement('button');
    guard_button.textContent = 'Guard';
    guard_button.classList.add('button', 'nonattack');
    guard_button.addEventListener('click', async () => {
        response = await fetch(`http://127.0.0.1:3000/fight/guard/0`);
        data = await response.json();
        updateStats();
        updateFight();
    });
    action_buttons.appendChild(guard_button);

    show(action_buttons);
    show(fight_div);
});

work_button.addEventListener('click', async () => {
    hideAll();

    response = await fetch('http://127.0.0.1:3000/work');
    data = await response.json();
    updateStats();

    const work_text = document.createElement('p');
    work_text.innerHTML = data.info[0].text;
    work_div.appendChild(work_text);

    return_button.textContent = 'OK';
    show(return_button);
    return_button.addEventListener('click', () => work_text.remove(), { once: true });

    show(action_buttons);
    show(work_div);
});

inv_button.addEventListener("click", () => {
    if (!shopping) {
        inv_div.classList.toggle("hidden");
    }
    achievement_div.classList.toggle("hidden");
});

return_button.addEventListener("click", () => {
    if (data.game_state.current_airport === "Ancient Chamber") {
        popupfunc("You can't return at this point.");
    } else {
        hideAll();
        removeActions();
        map_text.innerHTML = '';
        hide(return_button);
        show(main_buttons);
    }
});

shop_button.addEventListener("click", async () => {
    const shop_list = document.getElementById("shop_list");
    shop_list.innerHTML = "";

    shopping = true;
    hideAll();
    show(inv_div);

    const p = document.getElementById("shop_text");
    p.innerHTML = "&nbsp;";
    show(p);

    try {
        response = await fetch(`http://127.0.0.1:3000/shop/get/0`);
        data = await response.json();

        const arts = JSON.parse(data["info"][0]);

        for (let i = 0; i < arts.length; i++) {
            const art = arts[i];
            const b = document.createElement("button");
            b.classList.add("shop_button");
            b.textContent = `${art.name}\nValue: $${art.value}\nContinent: ${art["continent"]}`;

            b.addEventListener("click", async () => {
                response = await fetch(`http://127.0.0.1:3000/shop/buy/${i}`);
                data = await response.json();

                if (data["info"][0]["success"]) {
                    b.textContent = "Sold out!";
                    b.disabled = true;
                    await updateStats();
                }

                p.textContent = data["info"][0]["text"];
            }, { once: true });

            shop_list.appendChild(b);
        }

        for (let i = 0; i < inv_list.length; i++) {
            inv_list[i].disabled = false;
        }

        shop_div.appendChild(return_button);
        show(return_button);
        show(shop_list);
        show(shop_div);

        return_button.addEventListener("click", () => {
            action_buttons.appendChild(return_button);
            shopping = false;
            updateStats();
        }, { once: true });

    } catch (error) {
        console.log(error);
    }
});

// Initial load
depart();