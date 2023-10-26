from flask import Flask, render_template, url_for, request, jsonify
from datetime import time

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
    numbers = list(range(1, 15))
    times = ['12:30', '12:45', '13:00', '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00', '15:15',
             '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45', '18:00', '18:15',
             '18:30', '18:45', '19:00', '19:15', '19:30', '19:45', '20:00', '20:15', '20:30', '20:45', '21:00', '21:15',
             '21:30', '21:45', '22:00']
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

    response = (
        reservation.
        select().
        where(reservation.date == '-'.join(date_text)).
        order_by(reservation.hour)
    )

    for data in response:
        print(data.hour)


if __name__ == '__main__':
    app.run()
