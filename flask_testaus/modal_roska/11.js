'use strict';
let modal = document.getElementById("modal")
let modalpic = document.getElementById("modalpic")
let span = document.getElementsByTagName("span")[0]

// vie paljon tilaa mutta onpa luettavampi meille ihmisille
let art;
let h2;
let fig;
let img;
let figc;
let p;

const target = document.getElementById("pictures")

// joo ei toiminut kun yritti vaan muuttaa inner html arvoa :p
for (let i = 0; i < picArray.length; i++)
{
    // tee KAIKKI ja laita niihin oikeat arvot
    art = document.createElement("article");
    art.className = "card"

    h2 = document.createElement("h2")
    h2.textContent = picArray[i].title
    fig = document.createElement("figure")
    // img ja figc tähän
    img = document.createElement("img")
    img.src = picArray[i].image.medium
    figc = document.createElement("figcaption")
    figc.textContent = picArray[i].caption

    p = document.createElement("p")
    p.textContent = picArray[i].description

    fig.appendChild(img)
    fig.appendChild(figc)

    art.appendChild(h2)
    art.appendChild(fig)
    art.appendChild(p)


    art.onclick = function () {
        modalpic.src = picArray[i].image.large
        modal.style.display = "block";
    }


    target.appendChild(art)

}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";

  modal.style.scale = "1.03";
}
