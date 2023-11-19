const renderDataClient = function(dateText) {
    $.ajax({
        type: 'POST',
        url: '/api/get_client_information',
        data: JSON.stringify({
            "date_text": dateText,
        }),
        contentType: 'application/json',
        headers: {
          "Access-Token": localStorage.getItem("accessToken")
        },
        success: function(response, status) {
            const dataContents = $("#data_contents")
            dataContents.prop("innerHTML", response)
        }
    });
}

$(document).ready(function() {
    const dateBox = $("#datepicker")

    dateBox.datepicker({
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'],
        dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
        dateFormat: "dd/mm/yy",
        beforeShowDay: function(date) {
            let today = new Date(); // 获取当前日期和时间
            today.setHours(0, 0, 0, 0); // 将时间部分设置为零时零分零秒

            let currentDate = date.getTime();
            today = today.getTime();
            if (currentDate < today) {
                return [false, 'past-date'];
            } else {
                return [true, ''];
            }
        },
        onSelect: function (dateText) {
            renderDataClient(dateText)
        },
        onopen: function () {
            const selectedDate = $('#datepicker').datepicker('getDate');
            renderDataClient(initialDate)
            console.log('Selected Date on opening:', selectedDate);
        }
    });

    dateBox.datepicker("setDate", new Date());
});