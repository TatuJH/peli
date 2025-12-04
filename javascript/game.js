let response;
let data;
let update;

let map = null;

const left_div = document.getElementById('left_div');
const right_div = document.getElementById('right_div');
const main_buttons = document.getElementById('main_buttons');
const event_buttons = document.getElementById('event_buttons');


const getworkbtn = document.createElement('button');
getworkbtn.classList.add('button');
getworkbtn.textContent = 'WORK';

const getmapbtn = document.createElement('button');
getmapbtn.classList.add('button');
getmapbtn.textContent = 'MAP';

const geteventbtn = document.createElement('button');
geteventbtn.classList.add('button');
geteventbtn.textContent = 'EVENT';

const getfightbtn = document.createElement('button');
getfightbtn.classList.add('button');
getfightbtn.textContent = 'FIGHT';

main_buttons.appendChild(getworkbtn)
main_buttons.appendChild(getmapbtn)
main_buttons.appendChild(geteventbtn)
main_buttons.appendChild(getfightbtn)

// tää on nappi jota käytetään moneen eri asiaan o_O
const btn = document.createElement('button');
btn.classList.add('button');
btn.textContent = 'buton';
btn.classList.toggle("hidden", true)
right_div.appendChild(btn)

const stats_money = document.getElementById('money');
const stats_time = document.getElementById('time');
const stats_actions = document.getElementById('actions');

const invdiv = document.getElementById("inventory")
const invbutton = document.getElementById("inventory_button")

// tehdään nää vaan kerran
let event_div = document.getElementById("event_div")
let event_text = document.createElement('p');
let event_question = document.createElement('p');

event_div.appendChild(event_text);
event_div.appendChild(event_question);

const text = document.createElement('p');

// repun tekstielementit
let art_p_elements = [];

// laita ne kaikki vaan heti listaan
art_p_elements = document.getElementsByClassName("art");

//Initialize map
getmapbtn.addEventListener('click', async() => {

    hideAll(right_div)
    hideAll(left_div)

    if (map) {
        map.remove();
    }

    map = L.map('left_div', {
        worldCopyJump: false,
        minZoom: 2,
        maxZoom: 20
    }).setView([0, 0], 2);

    // map.setMaxBounds([
    //     [-90, -180],
    //     [90, 180]
    // ]);
    // map.on('drag', ()=> {
    //     map.panInsideBounds([
    //         [-90, -180],
    //         [90, 180]
    //     ], { animate: false });
    // });

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

    updateInventory(data);

    right_div.appendChild(text)
    //Add each airport to map
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

          btn.textContent = "DEPART"
          btn.addEventListener('click', async() => {

              //Let Flask know where user departed
              response = await fetch(`http://127.0.0.1:3000/airport/depart/${data.airports[i].aname}/${data.airports[i].cname}`);
              data = await response.json();

              updateInventory(data);

              //Clear divs and reinitialize
              hideAll(left_div)
              left_div.className = '';
              left_div.classList.add('main_div');
              hideAll(right_div)
              text.classList.toggle("hidden", true)
              btn.classList.toggle("hidden",true)
              toggleVisibility(main_buttons, true)
          },{ once: true });
          btn.classList.toggle("hidden", false)

          // TODO: placeholder !!!
          text.textContent = `Airport: ${data.airports[i]['aname']}, country: ${data.airports[i]['cname']}, size: ${data.airports[i]['type']}, latitude: ${data.airports[i]['latitude']}, longitude: ${data.airports[i]['longitude']}, ICAO: ${data.airports[i]['icao']}, continent: ${data.airports[i]['continent']}`;

          });

          //Add effects to circlemarker
          circle.on('mouseover', () => {
              circle.setStyle({fillOpacity : 0.5});
          });
          circle.on('mouseout', () => {
              circle.setStyle({fillOpacity : 1});
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

});



// todo inventory ja saavutukset tulee muiden PÄÄLLE, niin ei tarvii pitää kirjaa mitä niiden alla on
invbutton.addEventListener("click", async function(evt)
{
    toggleVisibility(invdiv)
});

// anna tälle elementti jonka haluat piilottaa tai näyttää
// true laittaa näkyviin, false piiloon, ei mitään tekee siitä togglen
function toggleVisibility(thing, bool = undefined)
{
    if(bool === true)
        thing.classList.toggle('hidden', false);
    else if (bool === false)
        thing.classList.toggle('hidden', true);
    else
        thing.classList.toggle('hidden');
}

// piilota KAIKKI annetun divin sisältö
// todo laita tää piilottamaan kaikki muutkin kuin divit
function hideAll(div)
{
    const children = div.querySelectorAll("div");
    children.forEach(div => {
        div.classList.toggle('hidden', true);
    })
}


geteventbtn.addEventListener('click', async() => {

    //Clear divs
    hideAll(left_div)
    hideAll(right_div)


    //Fetch random event from Python via Flask
    response = await fetch('http://127.0.0.1:3000/events/get/0/x');
    data = await response.json();

    // yksinkertaisesti muutetaan teksti ja laitetaan näkyville
    event_text.textContent = data.text;
    event_question.textContent = data.question;

    toggleVisibility(event_div, true)
    toggleVisibility(event_buttons, true)

    //Get choices and create button for each one
    for (let i = 0; i < data.choices.length; i++) {

        const eventbutton = document.createElement('button');
        eventbutton.textContent = data.choices[i];
        eventbutton.classList.add('button');
        event_buttons.appendChild(eventbutton)

        eventbutton.addEventListener('click', async() => {

            // jos eventti menee läpi
            if (data.money >= data.money_costs[i] && data.time >= data.time_costs[i] && data.artefacts >= data.artefacts_costs[i]) {


                //Fetch event results from Python via Flask
                response = await fetch(`http://127.0.0.1:3000/events/result/${data.number}/${data.choices[i]}`);
                data = await response.json();

                // kyssäri ja napit vittuun
                toggleVisibility(event_question, false)
                toggleVisibility(event_buttons, false)

                event_text.textContent = data.text;

                //Ok button takes back to menu

                btn.textContent = 'OK';
                btn.classList.toggle("hidden", false)
                btn.addEventListener('click', () => {

                    //Clear divs and reinitialize
                    event_buttons.innerHTML = ""
                    btn.classList.toggle("hidden", true)
                    hideAll(left_div)
                    // todo kaupunkimaisema lol
                    toggleVisibility(main_buttons, true)
                // KUN KÄYTETÄÄN NAPPEJA UUSIKSI, LISÄÄ ONCE : TRUE
                },{ once: true });

                // lisää reppunäkymään aarteet - muista parsettaa
                updateInventory(data)

            } else {
                event_text.innerHTML += '<br>Not enough resources';
            }

        });


    }

});


// käy läpi kaikki reppupaikat ja lisää artefaktin mikäli sellainen ON
function updateInventory(data)
{
    stats_money.textContent = `Money: ${data.money}`;
    stats_time.textContent = `Time: ${data.time}`;
    stats_actions.textContent = `Actions left: ${data.actions}`

    let arts = JSON.parse(data.all_artefacts)

    for (let i = 0; i < art_p_elements.length; i++) {

        if(arts[i]) {
            art_p_elements[i].textContent = `Artefact name: ${arts[i]["name"]} Value: $${arts[i]["value"]} Continent: ${arts[i]["continent"]}`
        } else {
            art_p_elements[i].textContent = "tyhjä repputila :D"
        }

    }

}

// TODO PÄIVITÄ TÄÄ UUTEEN SYSTEEMIIN
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

getworkbtn.addEventListener('click', async() => {

  hideAll(right_div);
  hideAll(left_div);

  response = await fetch('http://127.0.0.1:3000/work');
  data = await response.json();

  updateInventory(data);

  text.textContent = data.text;
  left_div.appendChild(text);

  btn.textContent = 'OK';
  btn.classList.toggle("hidden", false)
  btn.addEventListener('click', () => {

      //Clear divs and reinitialize
      hideAll(left_div)
      btn.classList.toggle("hidden", true)
      // todo kaupunkimaisema lol
      toggleVisibility(main_buttons, true)

  // KUN KÄYTETÄÄN NAPPEJA UUSIKSI, LISÄÄ ONCE : TRUE
  },{ once: true });

});
