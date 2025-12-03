let response;
let data;
let update;

const left_div = document.getElementById('left_div');
const right_div = document.getElementById('right_div');

const stats_money = document.getElementById('money')
const stats_time = document.getElementById('time')

// repun tekstielementit
let art_p_elements = [];

// laita ne kaikki vaan heti listaan
art_p_elements = document.getElementsByClassName("art");

//Initialize map
const getmapbtn = document.createElement('button');
getmapbtn.classList.add('button');
getmapbtn.textContent = 'MAP';
getmapbtn.addEventListener('click', async() => {

    right_div.innerHTML = '';
    left_div.innerHTML = '';

    var map = L.map('left_div', {
        worldCopyJump: false,
        minZoom: 2,
        maxZoom: 20
    }).setView([0, 0], 2);

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

    L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}{r}.{ext}', {
        minZoom: 0,
        maxZoom: 20,
        ext: 'png'
    }).addTo(map);

    //Fetch list of airports from database via Flask
    response = await fetch('http://127.0.0.1:3000/airport/get/0/0');
    data = await response.json();

    //Add each airport to map
    for (let i = 0; i < data.length; i++) {

        //Set colors for different airport types
        let color;

        if (i === 0) {
          color = "red";
        } else if (i === 1) {
          color = '#7CFC00';
        } else if (data[i].type === "large_airport") {
          color = "navy";
        } else if (data[i].type === "medium_airport") {
          color = "dodgerblue";
        } else if (data[i].type === "small_airport") {
          color = "lightskyblue";
        }

        //Initialize circlemarker AKA individual airport
        const circle = L.circleMarker(
            [data[i].latitude, data[i].longitude],
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

          right_div.innerHTML = '';

          //Initialize depart button
          const departbtn = document.createElement('button');
          departbtn.classList.add('button');
          departbtn.textContent = 'DEPART';
          departbtn.addEventListener('click', async() => {

              //Let Flask know where user departed
              update = await fetch(`http://127.0.0.1:3000/airport/depart/${data[i].aname}/${data[i].cname}`);

              //Clear divs and reinitialize
              left_div.innerHTML = '';
              left_div.className = '';
              left_div.classList.add('main_div');
              right_div.innerHTML = '';
              right_div.appendChild(geteventbtn);
              right_div.appendChild(getfightbtn);
              right_div.appendChild(getmapbtn);

          });

          // TODO: placeholder !!!
          const text = document.createElement('p');
          text.textContent = `Airport: ${data[i]['aname']}, country: ${data[i]['cname']}, size: ${data[i]['type']}, latitude: ${data[i]['latitude']}, longitude: ${data[i]['longitude']}, ICAO: ${data[i]['icao']}, continent: ${data[i]['continent']}`;
          right_div.appendChild(text);
          right_div.appendChild(departbtn);
          });

          //Add effects to circlemarker
          circle.on('mouseover', () => {
              circle.setStyle({fillOpacity : 0.5});
          });
          circle.on('mouseout', () => {
              circle.setStyle({fillOpacity : 1});
          });
          circle.bindTooltip(`${data[i].aname}`, {
              permanent: false,
              direction: 'top',
              sticky: true
          });

        } else {

            circle.bindTooltip(`You are currently in ${data[i].aname}`, {
                permanent: false,
                direction: 'top',
                sticky: true
            });

        }

    }

});

right_div.appendChild(getmapbtn);

//TODO nää pitää kattoo

// const invdiv = document.getElementById("inventory")
// const invbutton = document.getElementById("inventory_button")
// invbutton.addEventListener("click", async function(evt)
// {
//     //todo visibility of inventory
// });

//Initialize events
const geteventbtn = document.createElement('button');
geteventbtn.classList.add('button');
geteventbtn.textContent = 'EVENT';
geteventbtn.addEventListener('click', async() => {

    //Clear divs
    left_div.innerHTML = '';
    right_div.innerHTML = '';

    //Fetch random event from Python via Flask
    response = await fetch('http://127.0.0.1:3000/events/get/0/x');
    data = await response.json();

    //Display event text
    const event_text = document.createElement('p');
    event_text.textContent = data.text;
    left_div.appendChild(event_text);

    //Display event question
    const event_question = document.createElement('p');
    event_question.textContent = data.question;
    left_div.appendChild(event_question);

    //Get choices and create button for each one
    for (let i = 0; i < data.choices.length; i++) {

        const eventbutton = document.createElement('button');
        eventbutton.textContent = data.choices[i];
        eventbutton.classList.add('button');

        eventbutton.addEventListener('click', async() => {

            if (data.money >= data.money_costs[i] && data.time >= data.time_costs[i] && data.artefacts >= data.artefacts_costs[i]) {
                left_div.innerHTML = '';

                //Fetch event results from Python via Flask
                response = await fetch(`http://127.0.0.1:3000/events/result/${data.number}/${data.choices[i]}`);
                data = await response.json();

                event_text.textContent = data.text;
                left_div.appendChild(event_text);

                //Ok button takes back to menu
                const ok_button = document.createElement('button');
                ok_button.textContent = 'OK';
                ok_button.classList.add('button');
                ok_button.addEventListener('click', () => {

                    //Clear divs and reinitialize
                    left_div.innerHTML = '';
                    left_div.className = '';
                    left_div.classList.add('main_div');
                    right_div.innerHTML = '';
                    right_div.appendChild(geteventbtn);
                    right_div.appendChild(getfightbtn);
                    right_div.appendChild(getmapbtn);

                });

                right_div.innerHTML = '';
                right_div.appendChild(ok_button);

                // lisää reppunäkymään aarteet - muista parsettaa
                updateInventory(data)

            } else {

                const error = document.createElement('p');
                error.textContent = 'Not enough resources';
                left_div.appendChild(error);

            }

        });

        right_div.appendChild(eventbutton);

    }

});

right_div.appendChild(geteventbtn);

// käy läpi kaikki reppupaikat ja lisää artefaktin mikäli sellainen ON
function updateInventory(data)
{
    stats_money.textContent = `Money: ${data.money}`;
    stats_time.textContent = `Time: ${data.time}`;
    let arts = JSON.parse(data.all_artefacts)

    for (let i = 0; i < art_p_elements.length; i++) {

        if(arts[i]) {
            art_p_elements[i].textContent = `Artefact name: ${arts[i]["name"]} Value: $${arts[i]["value"]} Continent: ${arts[i]["continent"]}`
        } else {
            art_p_elements[i].textContent = "tyhjä repputila :D"
        }

    }

}

//Initialize fights
const getfightbtn = document.createElement('button');
getfightbtn.classList.add('button');
getfightbtn.textContent = 'FIGHT';
getfightbtn.addEventListener('click', async() => {

    function updateFight() {

        //Update page with new data
        document.getElementById('fighttxt').textContent = data.text;
        for (let i = 0; i < Object.keys(data.enemies_in_fight).length; i++) {

            if (data.enemies_in_fight[i].hp > 0) {
                    document.getElementById(`fightenemy${i}`).innerHTML = `Enemy ${i + 1}: ${data.enemies_in_fight[i].type} <span class="hp-text">${data.enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.enemies_in_fight[i].spd} turns)</span>`;
            }

        }

        document.getElementById('player').innerHTML = `HP: <span class="hp-text">${data.player_hp}</span>, remaining heals: <span class="ptn-text">${data.player_heals}</span>`;

    }

    left_div.innerHTML = '';
    right_div.innerHTML = '';

    //Fetch a fight starting position from Python via Flask
    response = await fetch('http://127.0.0.1:3000/fight/start/0');
    data = await response.json();

    //Create p element for tracking fight events
    const fight_text = document.createElement('p');
    fight_text.id="fighttxt";
    fight_text.textContent = data.text;
    left_div.appendChild(fight_text);

    //Create p element for tracking user
    const player = document.createElement('p');
    player.id="player";
    player.innerHTML = `HP: <span class="hp-text">${data.player_hp}</span>, remaining heals: <span class="ptn-text">${data.player_heals}</span>`;
    left_div.appendChild(player);

    //Create p elements for each enemy
    for (let i = 0; i < Object.keys(data.enemies_in_fight).length; i++) {

        const enemy = document.createElement('p');
        enemy.id=`fightenemy${i}`
        enemy.innerHTML = `Enemy ${i + 1}: ${data.enemies_in_fight[i].type} <span class="hp-text">${data.enemies_in_fight[i].hp}</span> <span class="spd-text">(charging for ${data.enemies_in_fight[i].spd} turns)</span>`;
        left_div.appendChild(enemy);

    }

    //Create button for attacking each enemy
    for (let i = 0; i < Object.keys(data.enemies_in_fight).length; i++) {

        const strike = document.createElement('button');
        strike.textContent = `Strike enemy ${i + 1} (${data.enemies_in_fight[i].type})`
        strike.classList.add('button');

        strike.addEventListener('click', async() => {

            //Update ongoing fight on Python via Flask
            response = await fetch(`http://127.0.0.1:3000/fight/strike/${i}`);
            data = await response.json();

            updateFight();

            //Remove enemy if defeated
            if (data.enemies_in_fight[i].hp <= 0) {

                left_div.removeChild(document.getElementById(`fightenemy${i}`));
                right_div.removeChild(strike);

            }

            //TODO when player defeated, add text etc
            if (data.player_hp <= 0) {

                //Clear divs and reinitialize
                left_div.innerHTML = '';
                left_div.className = '';
                left_div.classList.add('main_div');
                right_div.innerHTML = '';
                right_div.appendChild(geteventbtn);
                right_div.appendChild(getfightbtn);
                right_div.appendChild(getmapbtn);

            }

            //TODO when amount of enemies = 0, add text etc
            if (data.amount <= 0) {

                //Clear divs and reinitialize
                left_div.innerHTML = '';
                left_div.className = '';
                left_div.classList.add('main_div');
                right_div.innerHTML = '';
                right_div.appendChild(geteventbtn);
                right_div.appendChild(getfightbtn);
                right_div.appendChild(getmapbtn);

            }

        });

        right_div.appendChild(strike);

    }

    //Add heal button if user has potions
    if (data.player_heals > 0) {

        const heal = document.createElement('button');
        heal.textContent = 'Heal';
        heal.classList.add('button');

        heal.addEventListener('click', async() => {

            //Heal player, update Python via Flask
            response = await fetch(`http://127.0.0.1:3000/fight/heal/0`);
            data = await response.json();

            updateFight();

            //Remove heal button if user has no potions
            if (data['player_heals'] <= 0) {
                right_div.removeChild(heal);
            }

        });

        right_div.appendChild(heal);

    }

    //Make button for guarding
    const guard = document.createElement('button');
    guard.textContent = 'Guard';
    guard.classList.add('button');
    guard.addEventListener('click', async() => {

        //Update fight in Python via Flask
        response = await fetch(`http://127.0.0.1:3000/fight/guard/0`);
        data = await response.json();

        updateFight();

    });

    right_div.appendChild(guard);

});

right_div.appendChild(getfightbtn);