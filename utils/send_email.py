import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(data: dict):
    sender = 'z13646885180@gmail.com'
    password = 'marn blbp uhfl xivf'  # 这里是 Google 专用密码
    receivers = ['z635311808@icloud.com']  # 接收邮件的邮箱地址

    mail_msg = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
      <title>Reservar</title>
    </head>
    <body style="width: 100%; box-sizing: border-box; margin: 0; padding: 0">
      <div style="width: 100%; height: 2px; background-color: cornflowerblue; margin-top: 30px;"></div>
      <div style="padding: 0 20px">
        <h3 style="padding-left: 10px; text-align: left;">您有新的预约</h3>
        <hr style="width: 100%;">
        <h4>客户信息:</h4>

        <div style="width: 100%; height: auto; background-color: #e6e6e6">
        <div id="information_block" style="height: auto; margin-left: 20px; padding-top: 5px;">
          <p>Fecha: {data["date"]}</p>
          <div style="display: flex;">
            <p>Nombre: {data["name"]}</p>
            <p style="padding-left: 30px;">Apellido: {data["last_name"]}</p>
          </div>
          <p>TEL: {data["phone_number"]}</p>
          <div style="display: flex;">
            <p>Persona: {data["number_of_people"]}</p>
            <p style="padding-left: 30px;">Hora: {data["time_of_reserve"]}</p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("TUTUSTUDIO", 'utf-8')
    message['To'] = Header("OWNER", 'utf-8')

    subject = 'Reservar'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_obj.login(sender, password)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        smtp_obj.quit()
        return {
            'message': 'Enviado correctamente',
            'status': 200,
        }
    except smtplib.SMTPException as e:
        print("Error:", str(e))
