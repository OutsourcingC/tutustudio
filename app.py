from flask import Flask, render_template, url_for, request, jsonify

from peewee import fn
from database import db

from utils.match_pattern import match_pattern
from utils.send_email import send_email


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'


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


@app.route('/api/send_email', methods=['POST'])
def send_email_api():
    post_data = request.json

    if match_pattern(post_data):
        response = send_email(post_data)
    else:
        response = {
            'message': 'Input error',
            'status': 400,
        }

    return jsonify(response), response['status']


@app.route('/api/get_reserve_peaple', methods=["POST"])
def get_reserve_peaple():
    reservation = db.Reservation

    json_data = request.json
    date_text = json_data["date_text"].split('/')[::-1]
    reserve_time = json_data["reserve_time"]

    query = (
        reservation.
        select(reservation.hour, fn.SUM(reservation.people).alias('total_people')).
        where((reservation.date == '-'.join(date_text)) & (reservation.hour == reserve_time)).
        group_by(reservation.hour)
    )

    if query.get_or_none() is None:
        result = list(range(1, 11))
        isComplementFull = False
    else:
        result = query.get().total_people
        if result >= 10:
            result = ['Completamente lleno']
            isComplementFull = True
        else:
            result = list(range(1, 11-result))
            isComplementFull = False

    response = {
        'message': result,
        'isComplementFull': isComplementFull,
        'status': 200,
    }

    return jsonify(response), response['status']


if __name__ == '__main__':
    app.run()
