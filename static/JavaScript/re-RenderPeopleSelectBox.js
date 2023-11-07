
function ifComplementFull(data) {
    const people_box_select = document.querySelector("#people_box_select")
    people_box_select.innerHTML = `<option selected>${data[0]}</option>`
    people_box_select.disabled = true
}

function ifComplementFNotull(data) {
    const people_box_select = document.querySelector("#people_box_select")
    people_box_select.innerHTML = ''

    data.forEach(function (item) {
        var optionItem = document.createElement("option");

        optionItem.value = item;
        if (item === 1) {
            optionItem.textContent = item + " persona";
        } else {
            optionItem.textContent = item + " personas";
        }

        people_box_select.appendChild(optionItem);
    });
}

function getReversePeaple(dateText, reserveTime) {
    $.ajax({
        type: 'POST',
        url: '/api/get_reserve_peaple',
        data: JSON.stringify({
            "date_text": dateText,
            "reserve_time":reserveTime,
        }),
        contentType: 'application/json',
        success: function(response, status) {
            if (response.is_complement_full) {
                ifComplementFull(response.data)
            } else {
                ifComplementFNotull(response.data)
            }
        }
    });
}

$("#hour_box_select").change(function() {
    $('#people_box_select').prop("disabled", false);

    let selectedValue = $(this).val();
    let dateText = $("#datepicker").val()

    getReversePeaple(dateText, selectedValue)
});