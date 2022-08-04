let dark = document.querySelector('#dark');
let pastel = document.querySelector('#pastel');
let city = document.querySelector('#city');

dark.addEventListener('click', () =>{
    document.body.style.backgroundImage = "url('img/dark-theme.jpg')";
});

pastel.addEventListener('click', () =>{
    document.body.style.backgroundImage = "url('img/pastel.jpg')";
});

city.addEventListener('click', () =>{
    document.body.style.backgroundImage = "url('img/MyCoin-background.jpg')";
});