document.getElementById("toggleSidebar")
    .addEventListener("click", function () {
        document.querySelector(".sidebar")
            .classList.toggle("collapsed");
    });


const but = document.getElementById('toggleSidebar');
const cont = document.getElementById("container");

if (but && cont) {
    but.addEventListener('click', function () {
        cont.classList.toggle('expand');
    });
}

