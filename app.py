from flask import Flask, render_template, url_for, request, jsonify

from peewee import fn
from database import db
from datetime import time

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
    numbers = list(range(1, 11))
    times = ["11:00", "14:00", "17:00"]
    return render_template('reserve.html', numbers=numbers, times=times, favicon=favicon_img)


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


@app.route('/api/get_reserve_date', methods=["POST"])
def get_reserve_date():
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

    result = query.get()

    response = {
        'message': result.total_people,
        'status': 200,
    }

    return jsonify(response), response['status']


if __name__ == '__main__':
    app.run()
