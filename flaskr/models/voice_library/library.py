from flask import Flask, jsonify, Blueprint

app = Flask(__name__)
bp = Blueprint('library', __name__, url_prefix='/voices')
voices = [
    {'name': 'Mahesh', 'country': 'India'},
    {'name': 'Peter', 'country': 'USA'},
    {'name': 'Joe', 'country': 'UK'},
    {'name': 'Ahmed', 'country': 'UAE'},
]


@bp.route('/get-voices', methods=['GET'])
def get_voices():
    # Return the list of voices and their respective countries
    return jsonify(voices)
