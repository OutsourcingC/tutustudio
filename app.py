from flask import Flask, render_template, url_for, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import secrets

from peewee import fn
from database import db
from datetime import datetime, timedelta
import hashlib

from utils.match_pattern import match_pattern
from utils.send_email import send_email
from utils.login_verification import decrypt_cipher_text, account_validation
from utils.verify_jwt import validate_jwt_from_cookie

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
app.config['JWT_HEADER_NAME'] = 'Access-Token'  # 指定头部名为 access-token
app.config['JWT_HEADER_TYPE'] = ''  # 将认证方案设置为空字符串

JWT = JWTManager(app)

""" Web Page """
@app.route('/', methods=['GET'])
def home():
    favicon_img = url_for('static', filename='images/favicon.png')
    image_urls = [
        url_for('static', filename='images/1.jpg'),
        url_for('static', filename='images/2.jpg'),
        url_for('static', filename='images/3.jpg'),
        url_for('static', filename='images/4.jpg'),
        url_for('static', filename='images/5.jpg'),
        url_for('static', filename='images/6.jpg'),
    ]

    tutu_bcn_image_urls = [
        url_for('static', filename = 'images/tuftBCNimages/1.jpg'),
        url_for('static', filename = 'images/tuftBCNimages/2.jpg'),
    ]
    return render_template(
        'index.html',
        favicon=favicon_img,
        image_urls=image_urls,
        tutu_bcn_image_urls=tutu_bcn_image_urls,
    )


@app.route('/reserve', methods=['GET'])
def reserve():
    favicon_img = url_for('static', filename='images/favicon.png')
    people = list(range(1, 11))
    times = {
        "11:00": "11:00",
        "11:30": "11:00",
        "12:00": "11:00",
        "12:30": "11:00",
        "13:00": "11:00",
        "13:30": "11:00",
        "14:00": "14:00",
        "14:30": "14:00",
        "15:00": "14:00",
        "15:30": "14:00",
        "16:00": "14:00",
        "16:30": "14:00",
        "17:00": "17:00",
        "17:30": "17:00",
        "18:00": "17:00",
        "18:30": "17:00",
        "19:00": "17:00"
    }

    return render_template('reserve.html', people=people, times=times, favicon=favicon_img)


@app.route('/super_user_login', methods=['GET'])
def super_user_login():
    favicon_img = url_for('static', filename='images/favicon.png')

    return render_template('super_user_login.html', favicon=favicon_img)


""" API """
@app.route('/api/send_email', methods=['POST'])
def send_email_api():
    post_data = request.json

    if match_pattern(post_data):
        response = send_email(post_data)
    else:
        response = {
            'message': 'Input error',
            'status': 'error',
            'status_code': 400,
        }

    return jsonify(response), response['status_code']


@app.route('/api/get_reserve_peaple', methods=["POST"])
def get_reserve_peaple():
    json_data = request.json
    date_text = json_data["date_text"]
    reserve_hour = json_data["reserve_hour"]

    reservation = db.Reservation

    try:
        datetime.strptime(date_text, '%d/%m/%Y')
        datetime.strptime(reserve_hour, '%H:%M')

        query = (
            reservation.
            select(reservation.reserve_hour, fn.SUM(reservation.people).alias('total_people')).
            where((reservation.date == '-'.join(date_text.split('/')[::-1])) & (reservation.reserve_hour == reserve_hour)).
            group_by(reservation.reserve_hour)
        )

        if query.get_or_none() is None:
            result = list(range(1, 11))
            is_complement_full = False
        else:
            result = query.get().total_people
            if result >= 10:
                result = ['Completamente lleno']
                is_complement_full = True
            else:
                result = list(range(1, 11-result))
                is_complement_full = False

        response = {
            'message': 'petición exitosa',
            'data': result,
            'is_complement_full': is_complement_full,
            'status': "success",
            'status_code': 200,
        }
    except:
        response = {
            'message': 'parametro error',
            'data': None,
            'is_complement_full': None,
            'status': "error",
            'status_code': 400,
        }

    return jsonify(response), response['status_code']


@app.route('/api/super_user_login', methods=['POST'])
def api_super_user_login():
    encrypted_data = request.json

    username = encrypted_data['username']
    password = hashlib.sha256(decrypt_cipher_text(encrypted_data)).hexdigest()

    validation_result = account_validation(username = username, password = password)
    if not validation_result:
        response = {
            'message': '用户名或密码错误',
            'status': "error validation of account",
            'status_code': 400,
            'token': None,
        }
    else:
        additional_claims = {
            'sub': username,  # 用户标识
            'exp': datetime.utcnow() + timedelta(hours = 48)  # 有效时间为1小时
        }

        # 生成token
        access_token = create_access_token(
            identity = username,
            additional_claims = additional_claims
        )

        response = {
            'message': '登入成功',
            'status': "success",
            'status_code': 200,
            'token': access_token,
        }

    return response, response["status_code"]


""" Protected page"""
@app.route('/super_user/database_manager', methods=['GET'])
def database_manager():
    access_token = request.cookies.get('ACCESS_TOKEN')
    current_user, status_code, response = validate_jwt_from_cookie(access_token)

    if current_user is not None:
        favicon_img = url_for('static', filename='images/favicon.png')

        return render_template('database_manager.html', favicon = favicon_img)
    else:
        return response, status_code


''' Protected API '''
@app.route('/api/super_user/get_client_data', methods=['POST'])
@jwt_required()
def get_client_information():
    json_data = request.json
    date_text = json_data["date_text"]
    HTML_content = ''

    reservation = db.Reservation

    datetime.strptime(date_text, '%d/%m/%Y')

    query = (
        reservation.
            select().
            where(reservation.date == '-'.join(date_text.split('/')[::-1])).
            order_by(reservation.reserve_time)
    )

    if query.get_or_none() is None:
        HTML_content += f'''
        <div class="mt-3 pt-4" id="information_client" style="height: auto; text-align: center;">
            <h3>No hay ninguna ciente</h2>
            <p style="text-align: end; margin-right: 13px;">{date_text}</p>
        </div>'''
    else:
        for row in query:
            HTML_content += f'''
            <div class="mt-3 pt-4" id="information_client" client-id="{row.id}">
             <div class="px-3" id="information_detail">
                 <p>Nombre: {row.name}</p>
                 <p>Apellido: {row.last_name}</p>
                 <p>TEL: {row.phone}</p>
                 <p>Personas: {row.people}</p>
                 <p>Tiempo: {row.reserve_time}</p>
                 <div class="d-flex justify-content-between align-items-center pt-2" id="flex_box">
                     <button class="btn btn-primary" id="button_delete_data" onClick="deleteClientData(this)">Eliminar</button>
                     <p class="m-0">{row.date.strftime('%d/%m/%Y')}</p>
                 </div>
             </div>
         </div>'''

    return HTML_content


@app.route('/api/super_user/delete_client_data', methods=['POST'])
@jwt_required()
def delete_client_data():
    json_data = request.json
    client_id = json_data["client_id"]
    date_text = json_data["date_text"]

    reservation = db.Reservation

    try:
        client_to_delete = reservation.get((reservation.id == client_id) & (reservation.date == '-'.join(date_text.split('/')[::-1])))
        client_to_delete.delete_instance()
        response = {
            'message': '删除成功',
            'status': "success",
            'status_code': 200,
        }
    except reservation.DoesNotExist:
        response = {
            'message': '删除失败, 查询不到数据',
            'status': "error",
            'status_code': 400
        }

    return response

if __name__ == '__main__':
    app.run()
