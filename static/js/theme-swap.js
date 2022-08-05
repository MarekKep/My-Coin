let dark = document.querySelector('#dark');
let pastel = document.querySelector('#pastel');
let city = document.querySelector('#city');

dark.addEventListener('click', () =>{
    document.body.style.backgroundImage = 'url("https://cdn.wallpapersafari.com/5/24/IvSYOt.jpg")';
    document.body.style.color = "white";
});

pastel.addEventListener('click', () =>{
    document.body.style.backgroundImage = "url('https://img.freepik.com/free-vector/hand-painted-watercolor-pastel-sky-background_23-2148902771.jpg?w=2000')";
    document.body.style.backgroundSize = "cover";
});

city.addEventListener('click', () =>{
    document.body.style.backgroundImage = "url('img/MyCoin-background.jpg')";
});
