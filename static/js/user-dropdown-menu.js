// User menu

const userDropdown = document.querySelector(".user-icon");
const dropdownMenu = document.querySelector(".user-dropdown-menu");

userDropdown.addEventListener("click", () => {
    dropdownMenu.classList.toggle("hide");
});

window.addEventListener('click', (e) => {
    if (e.target !== userDropdown) {
        dropdownMenu.classList.add("hide");
    }
});
