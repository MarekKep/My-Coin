
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
});

document.querySelector(".nav-link").forEach(n => n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
}));

function oddEvenNumber(num) {
    var str = num.toString();
    var dict = {
      odd: 0,
      even: 0
      };
    for (let i = 0; i < str.length; i++) {
        if (parseInt(str.slice(i, i+1), 10) % 2 === 0) {
            dict["even"] += 1;
        }
        else{
            dict["odd"] += 1;
        }
}
    return dict;
}
console.log(oddEvenNumber(100500));