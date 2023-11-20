const accessToken = localStorage.getItem("accessToken")

const renderDataClient = function(dateText) {
    $.ajax({
        type: 'POST',
        url: '/api/super_user/get_client_data',
        data: JSON.stringify({
            "date_text": dateText,
        }),
        contentType: 'application/json',
        headers: {
          "Access-Token": accessToken
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
        }
    });

    dateBox.datepicker("setDate", new Date());
    const initialDate = $.datepicker.formatDate("dd/mm/yy", $("#datepicker").datepicker("getDate"));
    renderDataClient(initialDate)
});

function deleteClientData(buttonElement) {
    const clientId = $(buttonElement).parents("#information_client").attr('client-id')
    const dateText = $.datepicker.formatDate("dd/mm/yy", $("#datepicker").datepicker("getDate"))

    const userConfirmed = confirm("您确定要执行这个操作吗？");
    if (userConfirmed) {
        $.ajax({
            type: 'POST',
            url: '/api/super_user/delete_client_data',
            data: JSON.stringify({
                "client_id": clientId,
                "date_text": dateText
            }),
            contentType: 'application/json',
            headers: {
              "Access-Token": accessToken,
              "date_text": dateText,
            },
            success: function(response, status) {
                alert(response.message);
                renderDataClient(dateText)
            }
        });
    }
}