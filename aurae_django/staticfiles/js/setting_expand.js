const acc_overlay = document.getElementById("account_overlay");


document.getElementById("edit_account").addEventListener('click', function () {

    acc_overlay.showModal();

})
document.getElementById("close_but").addEventListener('click', function () {

    acc_overlay.close();

})


function expansion(but_id, content) {
    document.getElementById(but_id).classList.toggle("expand");
    document.getElementById(content).classList.toggle("show");
}