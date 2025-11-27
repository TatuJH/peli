let money = 1000;
let time = 365;
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



const eventdiv = document.getElementById('eventdiv');
const stats = document.getElementById("stats");
const geteventbtn = document.createElement("button");
geteventbtn.classList.add('button');
geteventbtn.id = 'event';
geteventbtn.textContent = 'EVENT';

eventdiv.appendChild(geteventbtn);

const eventbtn = document.getElementById("event");

eventbtn.addEventListener('click', async function(evt) {
    evt.preventDefault();

    eventdiv.innerHTML = '';

    response = await fetch('http://127.0.0.1:3000/getevent');
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
            if (money >= eventbutton.getAttribute('money') && time >= eventbutton.getAttribute('time')) {
                money = money - eventbutton.getAttribute('money');
            time = time - eventbutton.getAttribute('time');

            eventdiv.innerHTML = '';

            response = await fetch(`http://127.0.0.1:3000/eventresult/${data['number']}/${eventbutton.value}`);
            data = await response.json();

            money = money + data['money'];
            if (money < 0) {
                money = 0;
            }
            time = time + data['time'];
            if (time < 0) {
                time = 0;
            }

            const text = document.createElement('p');
            text.textContent = data['text'];
            eventdiv.appendChild(text);

            stats.textContent = `Money: ${money}, time: ${time}`;

            eventdiv.appendChild(eventbtn);
            } else {
                const error = document.createElement('p');
                error.textContent = 'Not enough resources';
                eventdiv.appendChild(error);

                eventdiv.appendChild(eventbtn);
            }
        })
        eventdiv.appendChild(eventbutton);
    }
});