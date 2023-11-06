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
            const reserveTime = $("#hour_box_select")
            reserveTime.prop("value", '-1')
        }
    });

    dateBox.datepicker("setDate", new Date());
});