//Removed obsolete variables, functions, etc.
//Added permanent elements instead of initializing them in JS; check HTML
//universal_button for simple tasks (OK-button, etc.)
//When adding eventListener to universal_button, use {once: true}
//Don't use classList.toggle, use either .add or .remove
//hideAll() hides all elements from right_div and left_div + additionally universal_button
//removeActions() removes all non-permanent action buttons (like event choices)
//updateInventory() now updateStats() for clarity
//Everything related to inventory (artefacts etc.) unchanged
//updateStats() after every fetch request

//--------------Variables--------------

//Initialize all Flask variables first so they can be referenced everywhere
let response;
let data;
let sub_data; //<--- Just in case

//Initialize map
let map = null;

//--------------------------------------------------------

//--------------Functions--------------

//Hides all relevant elements
function hideAll() {
    right_div.querySelectorAll('div').forEach(child => {
        child.classList.add('hidden');
    });

    left_div.querySelectorAll('div').forEach(child => {
        child.classList.add('hidden');
    });
    left_div.className = '';
    left_div.classList.add('split_screen');

    // go through all the buttons
    for (let i = 0; i < universal_buttons.length; i++)
    {
        hide(universal_buttons[i]);
    }

}

//Removes action buttons
function removeActions() {

    action_buttons.querySelectorAll('button').forEach(child => {

        if (!child.classList.contains('universal_button') && child.id !== "return_button") {
            child.remove();
        }

    });

}

//Updates all user stats on the page
function updateStats() {
    money_display.textContent = `Money: ${data.money}`;
    time_display.textContent = `Time: ${data.time}`;
    actions_display.textContent = `Actions left: ${data.actions}`


    if (data.all_artefacts) {

        let arts = JSON.parse(data.all_artefacts)

        for (let i = 0; i < inv_list.length; i++) {

            if (arts[i]) {
                inv_list[i].textContent = `Artefact name: ${arts[i]["name"]} \nValue: $${arts[i]["value"]}\nContinent: ${arts[i]["continent"]}`
            } else {
                inv_list[i].textContent = "tyhjä repputila :D"
            }

        }
    }

}

function hide(thing) {
    thing.classList.add('hidden');
}

function show(thing) {
    thing.classList.remove('hidden');
}
//--------------------------------------------------------

//--------------Permanent elements--------------

const main_div = document.getElementById("main");
const left_div = document.getElementById('left_div');
const right_div = document.getElementById('right_div');
const event_div = document.getElementById('event_div');
const fight_div = document.getElementById('fight_div');
const work_div = document.getElementById('work_div');
const map_div = document.getElementById('map_div');
const shop_div = document.getElementById('shop_div');
const inv_div = document.getElementById('inventory_div');
const achievement_div = document.getElementById('achievement_div');

const action_buttons = document.getElementById('action_buttons');
const main_buttons = document.getElementById('main_buttons');
const work_button = document.getElementById('work_button');
const event_button = document.getElementById('event_button');
const fight_button = document.getElementById('fight_button');
const map_button = document.getElementById('map_button');
const inv_button = document.getElementById('inv_button');
const return_button = document.getElementById("return_button");


// its a list incase we need more than 1 of them o_O
const universal_buttons = document.getElementsByClassName('universal_button');

const money_display = document.getElementById('money_display');
const time_display = document.getElementById('time_display');
const actions_display = document.getElementById('actions_display');


const inv_list = document.getElementsByClassName("art");

//--------------------------------------------------------

//--------------Permanent eventListeners--------------

//Initialize functionality for map button
map_button.addEventListener('click', async() => {

    hideAll()

    show(map_div)
    show(return_button)

    //Make sure map is reset
    if (map) {
        map.remove();
    }

    //Initialize map element
    map = L.map('map_div', {
        worldCopyJump: false,
        minZoom: 2,
        maxZoom: 20
    }).setView([0, 0], 2);

    //Stop map from scrolling too much
    map.setMaxBounds([
        [-90, -180],
        [90, 180]
    ]);
    map.on('drag', ()=> {
        map.panInsideBounds([
            [-90, -180],
            [90, 180]
        ], { animate: false });
    });

    // map styles

    // L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     maxZoom: 19,
    //     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright"></a>'
    // }).addTo(map);

    // L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    // attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    // }).addTo(map);

    //Add the "map" part to the map element
    L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}{r}.{ext}', {
        minZoom: 0,
        maxZoom: 20,
        ext: 'png'
    }).addTo(map);

    //Fetch list of airports from database via Flask
    response = await fetch('http://127.0.0.1:3000/airport/get/0/0');
    data = await response.json();

    updateStats();

    //Add a circle to the map for each airport
    for (let i = 0; i < data.airports.length; i++) {

        //Set colors for different airport types
        let color;

        if (i === 0) {
          color = "red";
        } else if (i === 1 && data.airports.length !== 19) {
          color = '#7CFC00';
        } else if (data.airports[i].type === "large_airport") {
          color = "navy";
        } else if (data.airports[i].type === "medium_airport") {
          color = "dodgerblue";
        } else if (data.airports[i].type === "small_airport") {
          color = "lightskyblue";
        }

        //Initialize circlemarker AKA individual airport
        const circle = L.circleMarker(
            [data.airports[i].latitude, data.airports[i].longitude],
            {
                opacity: 0,
                fillColor: color,
                fillOpacity: 1,
                radius: 15
            }
        ).addTo(map);

        //i === 0 same thing as the current airport
        if (i !== 0) {
          circle.addEventListener('click', () => {

              //Initialize depart button with the universal button element
              universal_buttons[0].textContent = "DEPART"
              universal_buttons[0].addEventListener('click', async () => {

                  //Let Flask know where user departed
                  response = await fetch(`http://127.0.0.1:3000/airport/depart/${data.airports[i].aname}/${data.airports[i].cname}`);
                  data = await response.json();

                  updateStats();

                  //Clear divs and reinitialize
                  hideAll();
                  universal_buttons[0].classList.add("hidden");
                  main_buttons.classList.remove("hidden");


              }, {once: true});
              show(universal_buttons[0])

          });

          //Add effects to circlemarker
          circle.on('mouseover', () => {
              circle.setStyle({fillOpacity: 0.5});
          });
          circle.on('mouseout', () => {
              circle.setStyle({fillOpacity: 1});
          });
          circle.bindTooltip(`${data.airports[i].aname}`, {
              permanent: false,
              direction: 'top',
              sticky: true
          });

        } else {

            circle.bindTooltip(`You are currently in ${data.airports[i].aname}`, {
                permanent: false,
                direction: 'top',
                sticky: true
            });

        }

    }

    action_buttons.classList.remove('hidden');

});

//Initialize functionality for event button
event_button.addEventListener('click', async() => {

    hideAll();

    //Fetch random event from Python via Flask
    response = await fetch('http://127.0.0.1:3000/events/get/0/x');
    data = await response.json();

    //Initialize non-permanent text element for events
    const event_text = document.createElement('p');
    event_text.innerHTML = `${data.text}<br><br>${data.question}`;
    event_div.appendChild(event_text);

    //Get choices and create non-permanent button for each one
    for (let i = 0; i < data.choices.length; i++) {

        const choice_button = document.createElement('button');
        choice_button.textContent = data.choices[i];
        choice_button.classList.add('button');
        choice_button.addEventListener('click', async() => {

            //Check whether user has enough resources
            if (data.money >= data.money_costs[i] && data.time >= data.time_costs[i] && data.artefacts >= data.artefacts_costs[i]) {

                //Fetch event results from Python via Flask
                response = await fetch(`http://127.0.0.1:3000/events/result/${data.number}/${data.choices[i]}`);
                data = await response.json();

                updateStats();

                removeActions();

                //Update event text
                event_text.textContent = data.text;

                //Initialize universal button for going back
                return_button.textContent = "OK";
                show(return_button)
                return_button.addEventListener('click', () => {
                    event_text.remove();

                    show(main_buttons)

                }, {once: true});

            } else {
                event_text.innerHTML += '<br>Not enough resources';
            }

        });

        action_buttons.appendChild(choice_button);

    }

    //Show everything
    show(action_buttons)
    show(event_div)

});

//Initialize functionality for fight button
fight_button.addEventListener('click', async() => {

    function updateFight() {

        //Update page with new data
        fight_text.innerHTML = `${data.text}<br><br>HP: <span class="hp-text">${data.player_hp}</span>, remaining heals: <span class="ptn-text">${data.player_heals}</span><br>`;
        for (let i = 0; i < Object.keys(data.enemies_in_fight).length; i++) {

            if (data.enemies_in_fight[i].hp > 0) {
                fight_text.innerHTML += `<br>Enemy ${i + 1}: ${data.enemies_in_fight[i].type} <span class="hp-text">${data.enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.enemies_in_fight[i].spd} turns)</span>`;
            }

        }

    }

    hideAll();

    //Fetch a fight starting position from Python via Flask
    response = await fetch('http://127.0.0.1:3000/fight/start/0');
    data = await response.json();

    updateStats();

    //Create non-permanent p element for tracking fight status
    const fight_text = document.createElement('p');
    fight_text.innerHTML = `${data.text}<br><br>HP: <span class="hp-text">${data.player_hp}</span>, remaining heals: <span class="ptn-text">${data.player_heals}</span><br>`;
    for (let i = 0; i < Object.keys(data.enemies_in_fight).length; i++) {

        fight_text.innerHTML += `<br>Enemy ${i + 1}: ${data.enemies_in_fight[i].type} <span class="hp-text">${data.enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.enemies_in_fight[i].spd} turns)</span>`;

    }
    fight_div.appendChild(fight_text);

    //Create non-permanent buttons for attacking each enemy
    for (let i = 0; i < Object.keys(data.enemies_in_fight).length; i++) {

        const strike_button = document.createElement('button');
        strike_button.textContent = `Strike enemy ${i + 1} (${data.enemies_in_fight[i].type})`
        strike_button.classList.add('button');
        action_buttons.appendChild(strike_button);

        strike_button.addEventListener('click', async() => {

            //Update ongoing fight on Python via Flask
            response = await fetch(`http://127.0.0.1:3000/fight/strike/${i}`);
            data = await response.json();

            updateStats();

            updateFight();

            //Remove enemy if defeated
            if (data.enemies_in_fight[i].hp <= 0) {

                action_buttons.removeChild(strike_button);

            }

            //TODO when player defeated, add text etc
            if (data.player_hp <= 0) {

                //Hides everything, takes user back to actions menu
                hideAll();
                removeActions();
                fight_div.querySelectorAll('p').forEach(child => {

                        child.remove();

                });

                updateStats();

                //TODO päänäkymä / kaupunki
                show(main_buttons)

            }

            //TODO when amount of enemies = 0, add text etc
            if (data.amount <= 0) {

                //Hides everything, takes user back to actions menu
                hideAll();
                removeActions();
                fight_div.querySelectorAll('p').forEach(child => {

                        child.remove();

                });

                updateStats();

                //TODO päänäkymä / kaupunki
                main_buttons.classList.remove('hidden');

            }

        });

    }

    //Add non-permanent heal button if user has potions
    if (data.player_heals > 0) {

        const heal_button = document.createElement('button');
        heal_button.textContent = 'Heal';
        heal_button.classList.add('button');
        heal_button.addEventListener('click', async() => {

            //Heal player, update Python via Flask
            response = await fetch(`http://127.0.0.1:3000/fight/heal/0`);
            data = await response.json();

            updateStats();

            updateFight();

            //Remove heal button if user has no potions
            if (data['player_heals'] <= 0) {

                action_buttons.removeChild(heal_button);

            }

        });

        action_buttons.appendChild(heal_button);

    }

    //Make non-permanent button for guarding
    const guard_button = document.createElement('button');
    guard_button.textContent = 'Guard';
    guard_button.classList.add('button');
    guard_button.addEventListener('click', async() => {

        //Update fight in Python via Flask
        response = await fetch(`http://127.0.0.1:3000/fight/guard/0`);
        data = await response.json();

        updateStats();

        updateFight();

    });

    action_buttons.appendChild(guard_button);

    //Show everything
    action_buttons.classList.remove('hidden');
    fight_div.classList.remove('hidden');


});

//Initialize functionality for work button
work_button.addEventListener('click', async() => {

    hideAll();

    //Fetch stats from working via Flask
    response = await fetch('http://127.0.0.1:3000/work');
    data = await response.json();

    updateStats();

    //Initialize non-permanent p element for work
    const work_text = document.createElement('p');
    work_text.textContent = data.text;
    work_div.appendChild(work_text);


    return_button.textContent = 'OK';
    show(return_button)
    return_button.addEventListener('click', () => {
        work_text.remove();
    },{once: true});

    //Show everything
    action_buttons.classList.remove('hidden');
    work_div.classList.remove('hidden');

});

inv_button.addEventListener("click", async function()
{
    inv_div.classList.toggle("hidden");
    achievement_div.classList.toggle("hidden");
});

return_button.addEventListener("click", async function()
{
    hideAll()
    hide(return_button)
    show(main_buttons)
});

async function achievements() {
    const achievements_list = document.getElementById('achievement_list');

    let response = await fetch('http://127.0.0.1:3000/ach');
    let data = await response.json();

    achievements_list.innerHTML = "";

    for (let i = 0; i < data.achievements.length; i++) {
        const li = document.createElement('li');
        li.textContent = data.achievements[i].name;
        li.title = data.achievements[i].description;
        li.className = "ach";
        achievements_list.appendChild(li);
    }
}

achievements()

