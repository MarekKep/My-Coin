let dark = document.querySelector('#dark');
let pastel = document.querySelector('#pastel');
let city = document.querySelector('#city');

const themeNameEnum = {
    city: '1',
    dark: '2',
    pastel: '3'
  };

let saveItem = localStorage.getItem('theme')
setTheme(saveItem);


dark.addEventListener('click', () =>{
    setTheme(themeNameEnum.city);
    saveTheme(themeNameEnum.city);
});

pastel.addEventListener('click', () =>{
    setTheme(themeNameEnum.dark);
    saveTheme(themeNameEnum.dark);
});

city.addEventListener('click', () =>{
    setTheme(themeNameEnum.pastel);
    saveTheme(themeNameEnum.pastel);
});

const saveTheme = (theme) => {
    localStorage.setItem('theme', theme);
}

function setTheme(themeName) {
    if (themeName == themeNameEnum.city) {
        document.body.style.backgroundImage = 'url("https://images.pexels.com/photos/114979/pexels-photo-114979.jpeg?cs=srgb&dl=pexels-veeterzy-114979.jpg&fm=jpg")';
    } else if (themeName == themeNameEnum.dark) {
        document.body.style.backgroundImage = "url('https://img.freepik.com/free-vector/hand-painted-watercolor-pastel-sky-background_23-2148902771.jpg?w=2000')"; 
    } else if (themeName == themeNameEnum.pastel) {
        document.body.style.backgroundImage = "url('https://audit-invest.com.ua/wp-content/uploads/2017/05/Savin-NY-Website-Background-Web1.jpg')";
    };
}