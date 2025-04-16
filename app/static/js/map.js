function toNumber(element) {
    return  Number(element.value ?? '0') || 1;
}

const shirota = document.getElementById('shirota');
const dolgota = document.getElementById('dolgota');
const third = document.getElementById('third');
const button = document.getElementById('btn');


const map = L.map('map');

button.addEventListener('click', ()=> {
    const shir = toNumber(shirota);
    const dol = toNumber(dolgota);
    const th = toNumber(third);
    map.setView([shir, dol], th); 
})


map.setView([51.710298, 46.748233], 11); 

L.tileLayer('Tiles/{z}/{x}/{y}.png', {
    maxZoom: 17,
    minZoom: 10,
    tileSize: 256,
    zoomOffset: 0,
    attribution: 'Your attribution goes here' 
}).addTo(map);