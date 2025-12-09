//Removed obsolete variables, functions, etc.
//Added permanent elements instead of initializing them in JS; check HTML
//return_button for simple tasks (OK-button, etc.)
//When adding eventListener to return_button, use {once: true}
//Don't use classList.toggle, use either .add or .remove
//hideAll() hides all elements from right_div and left_div + additionally return_button
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

//Random departure fix
let departHandler = null;

let shopping = true;

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

    hide(return_button);

    fight_div.querySelectorAll('p').forEach(child => {
        child.remove();
    });

}

//Removes action buttons
function removeActions() {

    action_buttons.querySelectorAll('button').forEach(child => {

        if (!child.classList.contains('return_button') && child.id !== "return_button" && child.id !== "depart_button") {
            child.remove();
        }

    });

}

//Updates all user stats on the page
async function updateStats() {
    money_display.textContent = `Money: ${data.game_state.money}`;
    time_display.textContent = `Time: ${data.game_state.time}`;
    actions_display.textContent = `Actions left: ${data.game_state.actions}`


    if (data.game_state.all_artefacts) {

        let arts = JSON.parse(data.game_state.all_artefacts)

        for (let i = 0; i < inv_list.length; i++) {

            if (arts[i]) {
                inv_list[i].textContent = `Artefact name: ${arts[i]["name"]} \nValue: $${arts[i]["value"]}\nContinent: ${arts[i]["continent"]}`
            } else {
                inv_list[i].textContent = "backpack slot :p"
            }

        }
    }

    // rahan nollauksesta ei häviä :p
    if (data.game_state.time <= 0 || data.game_state.actions < 0) {
        await fetch('http://127.0.0.1:3000/reset', { method: 'POST' });
        location.href = 'lose_screen.html';
    }
}

function hide(thing) {
    thing.classList.add('hidden');
}

function show(thing) {
    thing.classList.remove('hidden');
}

hide(popup);

function popupfunc(text) {

    show(popup);
    popup.textContent = text;
    setTimeout(() => {
        hide(popup);
        }, 3000);
}

async function depart() {

  hideAll()

    return_button.textContent = 'Return';
    show(map_container);
    show(map_div);
    show(map_text);
    show(return_button);

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

    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    }).addTo(map);

    // L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}{r}.{ext}', {
    //     minZoom: 0,
    //     maxZoom: 20,
    //     ext: 'png'
    // }).addTo(map);

    //Add the "map" part to the map element
    // L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.{ext}', {
	// minZoom: 1,
	// maxZoom: 16,
	// ext: 'jpg'
    // }).addTo(map);

    //Fetch list of airports from database via Flask
    response = await fetch('http://127.0.0.1:3000/airport/get/0/0/0/0/0');
    data = await response.json();

    updateStats();

    const maptext = document.createElement('p');
    maptext.textContent = "Select airport. The darker the blue, the larger the airport."
    map_text.appendChild(maptext);

    //Add a circle to the map for each airport
    for (let i = 0; i < data.info[0].length; i++) {

        //Set colors for different airport types
        let color;

        if (i === 0) {
          color = "red";
        } else if (i === 1 && data.info[0].length !== 19) {
          color = '#7CFC00';
        } else if (data.info[0][i].type === "large_airport") {
          color = "navy";
        } else if (data.info[0][i].type === "medium_airport") {
          color = "dodgerblue";
        } else if (data.info[0][i].type === "small_airport") {
          color = "lightskyblue";
        }

        //Initialize circlemarker AKA individual airport
        const circle = L.circleMarker(
            [data.info[0][i].latitude, data.info[0][i].longitude],
            {
                opacity: 0,
                fillColor: color,
                fillOpacity: 1,
                radius: 20
            }
        ).addTo(map);

        //i === 0 same thing as the current airport
        if (i !== 0) {
          circle.addEventListener('click', () => {

            depart_button.textContent = `${data.info[0][i].aname}, ${data.info[0][i].cname} (${data.info[0][i].alt_cont})`;
              //Initialize depart button
            const departHandler = async function() {

              if (data.game_state.money >= data.info[0][i].cost) {

                    //Let Flask know where user departed
                    response = await fetch(
                        `http://127.0.0.1:3000/airport/depart/${data.info[0][i].aname}/${data.info[0][i].cname}/${data.info[0][i].type}/${data.info[0][i].cost}/${data.info[0][i].continent}`);
                    data = await response.json();

                    updateStats();

                    //Clear divs and reinitialize
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
                    popup("Not enough money to fly!")
                  }
            }
            const departHover = function() {

              depart_button.textContent = "Depart";

            }
            const departOut = function() {

              depart_button.textContent = `${data.info[0][i].aname}, ${data.info[0][i].cname} (${data.info[0][i].alt_cont})`;

            }

              depart_button.addEventListener('click', departHandler, {once: true});
              depart_button.addEventListener('mouseover', departHover);
              depart_button.addEventListener('mouseout', departOut);

              show(return_button);
              show(depart_button);

          });

          //Add effects to circlemarker
          circle.on('mouseover', () => {
              circle.setStyle({fillOpacity: 0.5});
              maptext.innerHTML = `${data.info[0][i].aname}, ${data.info[0][i].cname} (${data.info[0][i].alt_cont}), <span class='moneytext'>$${data.info[0][i].cost}</span>`;
          });
          circle.on('mouseout', () => {
              circle.setStyle({fillOpacity: 1});
              maptext.textContent = "Select airport. The darker the blue, the larger the airport."
          });

        } else {

            circle.on('mouseover', () => {
              circle.setStyle({fillOpacity: 0.5});
              maptext.textContent = `You are currently in ${data.info[0][i].aname}, ${data.info[0][i].cname} (${data.info[0][i].alt_cont})`;
            });
            circle.on('mouseout', () => {
              circle.setStyle({fillOpacity: 1});
              maptext.textContent = "Select airport. The darker the blue, the larger the airport."
            });

        }

    }

    show(action_buttons);

}

async function achievements() {
    const achievements_list = document.getElementById('achievement_list');

    let response = await fetch('http://127.0.0.1:3000/ach');
    let data = await response.json();

    achievements_list.innerHTML = "";

    for (let i = 0; i < data.info[0].length; i++) {
        const li = document.createElement('li');

        li.textContent = data.info[0][i].name;

        li.className = "ach";
        achievements_list.appendChild(li);

        li.addEventListener('mouseover', () =>{
            li.textContent = data.info[0][i].description;
        });

        li.addEventListener('mouseout', () =>{
            li.textContent = data.info[0][i].name;
        });

        (function(ach, wait) {
            setTimeout(() => {
                show(popup);
                popup.textContent = `New achievement: ${data.info[0][i].name}`;

                setTimeout(() => {
                    hide(popup);
                }, 3000);

            }, wait);
        })(data.info[0][i], i * 3500);
    }
}

//--------------------------------------------------------

//--------------Permanent elements--------------

const main_div = document.getElementById("main");
const left_div = document.getElementById('left_div');
const right_div = document.getElementById('right_div');
const event_div = document.getElementById('event_div');
const fight_div = document.getElementById('fight_div');
const work_div = document.getElementById('work_div');
const map_container = document.getElementById('map_container');
const map_div = document.getElementById('map_div');
const map_text = document.getElementById('map_text');
const shop_div = document.getElementById('shop_div');
const inv_div = document.getElementById('inventory_div');
const achievement_div = document.getElementById('achievement_div');

const action_buttons = document.getElementById('action_buttons');
const main_buttons = document.getElementById('main_buttons');
const work_button = document.getElementById('work_button');
const event_button = document.getElementById('event_button');
const fight_button = document.getElementById('fight_button');
const shop_button = document.getElementById("shop_button");
const map_button = document.getElementById('map_button');
const inv_button = document.getElementById('inv_button');
const return_button = document.getElementById("return_button");
const depart_button = document.getElementById('depart_button');

const money_display = document.getElementById('money_display');
const time_display = document.getElementById('time_display');
const actions_display = document.getElementById('actions_display');


const inv_list = document.getElementsByClassName("art");

//--------------------------------------------------------

//--------------Permanent eventListeners--------------

//Initialize functionality for map button
map_button.addEventListener('click', async() => {

    depart();

});

//Initialize functionality for event button
event_button.addEventListener('click', async() => {

    hideAll();
    hide(return_button);

    //Fetch random event from Python via Flask
    response = await fetch('http://127.0.0.1:3000/events/get/0/x');
    data = await response.json();

    //Initialize non-permanent text element for events
    const event_text = document.createElement('p');
    event_text.innerHTML = `${data.info[0].text}<br><br>${data.info[0].question}`;
    event_div.appendChild(event_text);

    //Get choices and create non-permanent button for each one
    for (let i = 0; i < data.info[0].choices.length; i++) {

        const choice_button = document.createElement('button');
        choice_button.textContent = data.info[0].choices[i];
        choice_button.classList.add('button');
        choice_button.addEventListener('click', async() => {

            //Check whether user has enough resources
            if (data.game_state.money >= data.info[0].money_costs[i] && data.game_state.time >= data.info[0].time_costs[i] && data.game_state.artefacts >= data.info[0].artefacts_costs[i]) {

                //Fetch event results from Python via Flask
                response = await fetch(`http://127.0.0.1:3000/events/result/${data.info[0].number}/${data.info[0].choices[i]}`);
                data = await response.json();

                updateStats();

                removeActions();

                //Update event text
                event_text.innerHTML = data.info[0].text;

                //Initialize universal button for going back
                return_button.textContent = "OK";
                show(return_button)
                return_button.addEventListener('click', () => {
                    event_text.remove();

                    show(main_buttons)

                }, {once: true});

            } else {
                popupfunc("Not enough resources!")
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
        fight_text.innerHTML = `${data.info[0].text}<br><br>HP: <span class="hp-text">${data.info[0].player_hp}</span>, remaining heals: <span class="ptn-text">${data.info[0].player_heals}</span><br>`;
        for (let i = 0; i < Object.keys(data.info[0].enemies_in_fight).length; i++) {

            if (data.info[0].enemies_in_fight[i].hp > 0) {
                fight_text.innerHTML += `<br>Enemy ${i + 1}: ${data.info[0].enemies_in_fight[i].type} <span class="hp-text">${data.info[0].enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.info[0].enemies_in_fight[i].spd} turns)</span>`;
            }

        }

        if (data.info[0].player_hp <= 0) {

            removeActions();
            fight_div.querySelectorAll('p').forEach(child => {

                    child.remove();

            });

            return_button.textContent = "OK";
            show(return_button)

            fight_text.innerHTML = "One of the heretics knocks you out for <span class='timetext'>10 days</span>."
            fight_div.appendChild(fight_text);

            updateStats();

    }

        if (data.info[0].amount <= 0) {

            removeActions();
            fight_div.querySelectorAll('p').forEach(child => {

                    child.remove();

            });

            return_button.textContent = "OK";
            show(return_button)

            fight_text.innerHTML = `You convert all the heretics. Your god is pleased and blesses you with <span class='timetext'>$${data.info[0].money_get}</span>.`
            fight_div.appendChild(fight_text);

            updateStats();

        }

    }

    hideAll();
    hide(return_button);

    //Fetch a fight starting position from Python via Flask
    response = await fetch('http://127.0.0.1:3000/fight/start/0');
    data = await response.json();

    updateStats();

    //Create non-permanent p element for tracking fight status
    const fight_text = document.createElement('p');
    fight_text.innerHTML = `${data.info[0].text}<br><br>HP: <span class="hp-text">${data.info[0].player_hp}</span>, remaining heals: <span class="ptn-text">${data.info[0].player_heals}</span><br>`;
    for (let i = 0; i < Object.keys(data.info[0].enemies_in_fight).length; i++) {

        fight_text.innerHTML += `<br>Enemy ${i + 1}: ${data.info[0].enemies_in_fight[i].type} <span class="hp-text">${data.info[0].enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.info[0].enemies_in_fight[i].spd} turns)</span>`;

    }
    fight_div.appendChild(fight_text);

    //Create non-permanent buttons for attacking each enemy
    for (let i = 0; i < Object.keys(data.info[0].enemies_in_fight).length; i++) {

        const strike_button = document.createElement('button');
        strike_button.textContent = `Strike enemy ${i + 1} (${data.info[0].enemies_in_fight[i].type})`
        strike_button.classList.add('button');
        strike_button.classList.add('attack');
        action_buttons.appendChild(strike_button);

        strike_button.addEventListener('click', async() => {

            //Update ongoing fight on Python via Flask
            response = await fetch(`http://127.0.0.1:3000/fight/strike/${i}`);
            data = await response.json();

            updateStats();

            updateFight();

            //Remove enemy if defeated
            if (data.info[0].enemies_in_fight[i].hp <= 0) {

                action_buttons.removeChild(strike_button);

            }

        });

    }

    //Add non-permanent heal button if user has potions
    if (data.info[0].player_heals > 0) {

        const heal_button = document.createElement('button');
        heal_button.textContent = 'Heal';
        heal_button.classList.add('button');
        heal_button.classList.add('nonattack');
        heal_button.addEventListener('click', async() => {

            //Heal player, update Python via Flask
            response = await fetch(`http://127.0.0.1:3000/fight/heal/0`);
            data = await response.json();

            updateStats();

            updateFight();

            //Remove heal button if user has no potions
            if (data.info[0].player_heals <= 0) {

                action_buttons.removeChild(heal_button);

            }

        });

        action_buttons.appendChild(heal_button);

    }

    //Make non-permanent button for guarding
    const guard_button = document.createElement('button');
    guard_button.textContent = 'Guard';
    guard_button.classList.add('button');
    guard_button.classList.add('nonattack');
    guard_button.addEventListener('click', async() => {

        //Update fight in Python via Flask
        response = await fetch(`http://127.0.0.1:3000/fight/guard/0`);
        data = await response.json();

        updateStats();

        updateFight();

    });

    action_buttons.appendChild(guard_button);

    //Show everything
    show(action_buttons);
    show(fight_div);


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
    work_text.innerHTML = `${data.info[0].text}`;
    work_div.appendChild(work_text);


    return_button.textContent = 'OK';
    show(return_button)
    return_button.addEventListener('click', () => {
        work_text.remove();
    },{once: true});

    //Show everything
    show(action_buttons);
    show(work_div);

});

inv_button.addEventListener("click", async function()
{
    if(!shopping)
        inv_div.classList.toggle("hidden");

    achievement_div.classList.toggle("hidden");
});

return_button.addEventListener("click", async function()
{
  if (data.info[0][0].aname === "Ancient Chamber") {

    popupfunc("You can't return at this point.")

  } else {

      hideAll();
      removeActions();
      map_text.innerHTML = '';
      hide(return_button);
      show(main_buttons);

  }

});


shop_button.addEventListener("click", async function() {

    // pelaaja menee kauppaan
    shop_div.innerHTML = ""

    // pelaaja ei voi togglata reppunäkymää, jos on kaupassa :p
    shopping = true;

    hideAll();

    show(inv_div);
    show(shop_div);


    try {

        // get luo kaupan python puolella
        response = await fetch(`http://127.0.0.1:3000/shop/get/0`);
        console.log(response)
        data = await response.json();
        console.log(data);

        // Iteroidaan kaikkien kaupan aarteiden läpi ja laitetaan ne kauppa diviin
        for (let i = 0; i < data.length; i++) {
            const art = data[i]
            const b = document.createElement("button");
            b.textContent = `${art.name}\nValue: $${art.value}\nContinent: ${art["continent"]}`

            // kun kauppanappia painetaan !!
            b.addEventListener("click", async function (evt) {
                // laitetaan jokaiselle kauppaesineelle käytännössä oma indeksi linkin myötä :-)
                response = await fetch(`http://127.0.0.1:3000/shop/buy/${i}`);
                data = await response.json();

                // python puolelta tulee datan mukana info joka kertoo menikö myynti läpi
                if(data["info"][0]["success"])
                {
                    // nappi veks päältä kun aarre on kaupattu
                    b.textContent = "Sold out!"
                    updateStats();
                    b.disabled = true;
                }

                p.textContent = data["info"][0]["text"]


            }, {once: true});
            shop_div.appendChild(b);
        }
        // tehdään throwaway tekstielementti joka antaa palautetta pelaajalle
        const p = document.createElement("p")
        shop_div.appendChild(p)

        // inventaario diviin tulee lähe vetään nappi
        shop_div.appendChild(return_button)
        show(return_button)

        // return nappi hetkellisesti laitetaan kauppaan, kun kaupasta lähdetään palauta se ennalleen
        return_button.addEventListener("click", async function(evt){
            action_buttons.appendChild(return_button)
        },{once: true});

    }
    catch(error)
        {
           console.log(error)
        }




});

achievements()

depart();