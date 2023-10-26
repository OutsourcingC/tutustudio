function getReverseDate (dateText) {
    $.ajax({
        type: 'POST',
        url: '/api/get_reserve_date',
        data: JSON.stringify({
            "order_time": dateText
        }),
        contentType: 'application/json',
    });
}

$(document).ready(function () {
    const dateBox = $("#datepicker")
    getReverseDate(dateBox.value) // 初始化, 首次刷新

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
            getReverseDate(dateText) // 每次更新日期刷新
        }
    });

    dateBox.datepicker("setDate", new Date());
});