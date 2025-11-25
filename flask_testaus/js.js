let money = 0;
let response = "";
let data = "";

const eventText = document.getElementById('eventText');

const stats = document.getElementById('stats');

const buttons = document.getElementsByClassName('button');

for (let button of buttons) {
    button.addEventListener('click', (evt) => {
        evt.preventDefault()
        a(button.name, button.value);
    });
}


async function a(action, number) {
    if (action === "event") {
        response = await fetch(`http://127.0.0.1:3000/${action}/${number}`);
        data = await response.json();
        update(data)
    }
    else if (action === "scores") {
        response = await fetch(`http://127.0.0.1:3000/${action}`);
        data = await response.json();
        update(data)
    }
}

function update(info) {
    eventText.textContent = info['text'];
    stats.textContent = 'Money: ' + info['money'];
}

