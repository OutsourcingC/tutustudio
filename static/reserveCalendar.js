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
  });

  dateBox.datepicker("setDate", new Date());
});