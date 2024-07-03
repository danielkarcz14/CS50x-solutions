document.addEventListener("DOMContentLoaded", (event) => {
    var editBtns = document.querySelectorAll(".edit");
    var closeBtns = document.querySelectorAll(".close.cancel");
    var popups = document.querySelectorAll(".edit-popup");


    editBtns.forEach(function(btn, index) {
        btn.addEventListener('click', function() {
            openPopup(index);
        });
    });

    closeBtns.forEach(function(btn, index) {
        btn.addEventListener('click', function() {
            event.preventDefault();
            closePopup(index);
        });
    });


    function openPopup(index) {
        if (popups[index].style.display === "none") {
            popups[index].style.display = "block";
            } else {
                popups[index].style.display = "none";
            }
    }

    function closePopup() {}
    popups.forEach(function(popup) {
        var buttons = popup.querySelectorAll('.close.cancel');
        buttons.forEach(function(button) {
            button.addEventListener('click', function() {
                popup.style.display = 'none';
            });
        });
    });

    const updateSliders = (container) => {
        const inputSliders = container.querySelectorAll("input[type='range']");
        const valueDisplays = container.querySelectorAll(".value span");

        inputSliders.forEach((slider, index) => {
            slider.oninput = () => {
                let value = slider.value;
                let displayText = value + " €";
                if (slider.id === "slider-percentage-interest") {
                    displayText = value + " %";
                }
                if (slider.id === "slider-time") {
                    displayText = value + (value === 1 ? " year" : " years");
                }
                valueDisplays[index].textContent = displayText;

                updateResult(container);
            };
        });
    };

    const updateResult = (container) => {
        const monthValue = parseFloat(container.querySelector("#slider-eur-month").value);
        const time = parseFloat(container.querySelector("#slider-time").value);
        const extraDeposit = parseFloat(container.querySelector("#slider-eur-deposit").value);
        const interest = parseFloat(container.querySelector("#slider-percentage-interest").value);
        const result = calculateResult(monthValue, time, extraDeposit, interest);
        const resultInput = container.querySelector(".result input");
        resultInput.value = result + " €";
    };

    const calculateResult = (monthValue, time, extraDeposit, interest) => {
        const perAnnualInterestRate = interest / 100 + 1;
        const monthlyInterestRate = Math.pow(perAnnualInterestRate, 1/12) - 1;
        const months = time * 12;

        const futureMonthValue = monthValue * ((Math.pow(1 + monthlyInterestRate, months) - 1) / monthlyInterestRate) * (1 + monthlyInterestRate);

        const futureValueExtraDeposit = extraDeposit * Math.pow(1 + monthlyInterestRate, months);

        const totalFutureValue = futureMonthValue + futureValueExtraDeposit;

        return totalFutureValue.toFixed(2);
    };

    popups.forEach(popup => updateSliders(popup));

    const standaloneForm = document.querySelector("#standalone-form"); 
    if (standaloneForm) {
        updateSliders(standaloneForm);
    }


    $('.change').click(function(){
        var data = {};
        $('.set').each(function(){
            var key = $(this).attr("name");
            var value = $(this).val()
            data[key] = value;
        });

                
        $.ajax({
            url: '/settings',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(data),
            error: function( error) {
              //  console.log("Error: ", error);
            },
            success: function(response) {
                var messagess = response.messagess;
                messagessLabels = $(".message");

                var messagessLabelsMap = new Map()

                for (var i = 0; i < messagessLabels.length; i++) {
                    var key = messagessLabels[i].className.split(' ')[1];
                    messagessLabelsMap.set(key, messagessLabels[i]);
                }

                for (const [key, value] of Object.entries(messagess)) {
                    // console.log(`${key}: ${value}`)
                    if (messagessLabelsMap.has(key)) {
                        messagessLabelsMap.get(key).textContent = value;
                    }
                }
            }
        });

    });
    

    $('.download').click(function() {
        var data = {}
        $(this).closest('tr').find('.data').each(function(){
            var key = $(this).attr("name");
            data[key] = $(this).val()
        });
        console.log(data);
        $.ajax({
            url: '/myplans',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(data),
            error: function( error) {
                console.log("Error: ", error);
            },
            success: function(response) {
                console.log("success")
            }
        });

    });

    const toggleButton = document.querySelector('[data-collapse-toggle]');
    const menu = document.getElementById('navbar-sticky');

    toggleButton.addEventListener('click', function () {
      menu.classList.toggle('hidden');
    });

    function startDownload() {
        document.getElementById('waitMessage').style.display = 'block';
    
        fetch('/remove-file')
            .then(response => response.text())
            .then(() => {
                setTimeout(() => {
                    window.location.href = '/download';
                }, 8000);
            });
    }

    $('#download').click(function(){
        startDownload();
    });
});
