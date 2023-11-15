from flask import Flask, render_template, url_for, request, jsonify

from peewee import fn
from database import db
from datetime import datetime
import hashlib

from utils.match_pattern import match_pattern
from utils.send_email import send_email
from utils.login_verification import decrypt_cipher_text, account_validation

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'


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
    return render_template('index.html', image_urls=image_urls, favicon=favicon_img)


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
    reserve_time = json_data["reserve_time"]

    reservation = db.Reservation

    try:
        datetime.strptime(date_text, '%d/%m/%Y')
        datetime.strptime(reserve_time, '%H:%M')

        query = (
            reservation.
            select(reservation.hour, fn.SUM(reservation.people).alias('total_people')).
            where((reservation.date == '-'.join(date_text.split('/')[::-1])) & (reservation.hour == reserve_time)).
            group_by(reservation.hour)
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
        }
    else:


    return response, response["status_code"]


if __name__ == '__main__':
    app.run()
