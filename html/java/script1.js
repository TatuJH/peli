'use strict'

const instructions = document.querySelector('#instructions');
instructions.addEventListener('click', function(evt){
  location.href = "instructions.html";
});

const scores = document.querySelector('#scores');
scores.addEventListener('click', function(evt){
  location.href = "scores.html";
});

const start = document.querySelector('#start');
start.addEventListener('click', function(evt){
  location.href = "main.html";
});