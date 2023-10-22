function sendEmail() {
  const formData = {
  date: $('input[name="date"]').val(),
  name: $('input[name="name"]').val(),
  last_name: $('input[name="lastName"]').val(),
  phone_number: $('input[name="phoneNumber"]').val(),
  number_of_people: $('select[name="numberOfPeople"]').val(),
  time_of_reserve: $('select[name="time"]').val()
  };

  // 发送 POST 请求到 API
  $.ajax({
    type: 'POST',
    url: '/send_email',
    data: JSON.stringify(formData),
    contentType: 'application/json',
    success: function(response) {
      alert(response.message)
    },
    error: function(response) {
      alert(response.responseJSON.message)
    }
  });
}

function addValidation(boxId) {
  const box = document.getElementById(boxId);

  box.setCustomValidity('Necesario');

  box.addEventListener('input', function () {
    if (!box.value) {
      box.setCustomValidity('Necesario');
    } else if (box.validity.patternMismatch) {
      box.setCustomValidity('Por favor ingresa el formato correcto');
    } else {
      box.setCustomValidity(''); // 清空自定义验证消息
    }
  });
}

function validateHourSelect() {
  const selectElement = document.getElementById('hour_box_select');
  if (selectElement.value === '-1') {
    selectElement.setCustomValidity('Seleccione una hora.');
    selectElement.reportValidity(); // 显示自定义错误消息
  } else {
    selectElement.setCustomValidity('');
  }
}

document.addEventListener("DOMContentLoaded", function () {
  addValidation("name_box");
  addValidation("lastName_box");
  addValidation("phone_number_box");

  document.getElementById('hour_box_select').addEventListener('change', validateHourSelect);
  document.getElementById('form_reserve').addEventListener('submit', function (e) {
    validateHourSelect(); // 在表单提交前再次验证
    if (document.getElementById('hour_box_select').checkValidity() === false) {
      e.preventDefault(); // 阻止表单提交
    } else {
      e.preventDefault()
      sendEmail()
    }
  });
});


