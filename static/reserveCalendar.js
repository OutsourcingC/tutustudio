function getReverseDate (dateText, reserveTime) {
    console.log(reserveTime)
    $.ajax({
        type: 'POST',
        url: '/api/get_reserve_date',
        data: JSON.stringify({
            "date_text": dateText,
            "reserve_time":reserveTime,
        }),
        contentType: 'application/json',
    });
}

$(document).ready(function () {
    const dateBox = $("#datepicker")

    dateBox.datepicker({
        dateFormat: "dd/mm/yy",
        beforeShowDay: function (date) {
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
            getReverseDate(dateText, reserveTime.val()) // 每次更新日期刷新
        }
    });

    dateBox.datepicker("setDate", new Date());

    getReverseDate($.datepicker.formatDate('dd/mm/yy', dateBox.datepicker('getDate'))) // 初始化, 首次刷新
});