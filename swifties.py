from flask import Flask, jsonify, render_template, request, send_from_directory

import random

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

view_id = ''
view_count = 0
view_started = False

def start_new_session():
    global view_id, view_started

    view_id = hex(random.getrandbits(128))[2:-1]
    view_started = False

@app.route('/counters.js')
def send_js():
    return render_template('counters.js', v=view_id)

@app.route("/")
def index():
    start_new_session()
    return render_template("index.html", v=view_id, view_count=view_count)

@app.route("/start", methods=["POST"])
def start_view():
    global view_started
    body = request.get_json()
    if body:
      view_id_param = body.get('id')
      view_started = view_id == view_id_param
    return jsonify({'success': view_started})

@app.route("/count", methods=["POST"])
def count():
    global view_count
    is_valid_count = False
    if view_started:
        body = request.get_json()
        if body:
            view_id_param = body.get('id')
            is_valid_count = view_id == view_id_param
    if is_valid_count:
        view_count += 1
    start_new_session()
    return jsonify({'success': is_valid_count})
