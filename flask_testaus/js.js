let money = 0;
let response = "";
let data = "";

const text = document.getElementById('text');

const stats = document.getElementById('stats');

const buttons = document.getElementsByClassName('button');

for (let button of buttons) {
  button.addEventListener('click', (evt) => {
    evt.preventDefault()
    a(button.name, button.value);
  });
}

async function a(action, number) {
  response = await fetch(`http://127.0.0.1:3000/${action}/${number}`);
  data = await response.json();
  update(data)
}

function update(info) {
  text.textContent = info['text'];
  stats.textContent = 'Money: ' + info['money'];
}



