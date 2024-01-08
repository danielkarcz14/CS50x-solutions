document.addEventListener('DOMContentLoaded', function () {
    function blink() {
        let cursor = document.querySelector('.cursor');
        if (cursor.style.visibility == 'hidden') {
            cursor.style.visibility = 'visible';
        }
        else {
            cursor.style.visibility = 'hidden';
        }
    }
    setInterval(blink, 500)

    let divEdu = document.querySelector('.education');
    let divExp = document.querySelector('.experience');
    // set default display for exp section
    divExp.style.display = "none";

    document.querySelector('#edu').addEventListener('click', function(){
        divExp.style.display = "none";
        if (divEdu.style.display === "none") {
            divEdu.style.display = "flex";
        }
    })

    document.querySelector('#exp').addEventListener('click', function(){
        divEdu.style.display = "none";
        if (divExp.style.display === "none") {
            divExp.style.display = "flex";
        }
    })

    let buttons = document.querySelectorAll('.buttons button')

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            // remove active class
            buttons.forEach(function(btn) {
                btn.classList.remove('active');
            });
            // add active class
            button.classList.add('active');
        });
    });
});
