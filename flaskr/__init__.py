# from app import app
import os.path
import boto3
from flask_api import status
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager

from .models import landing_pages
from .models.texttovideo import to_video
from .models.effy_vision import video_tagging
from .models.upload_data import get_db, ENV
from .models.voice_library import library

app = Flask(__name__)
app.secret_key = 'super secret key'
db = get_db()
if ENV == "dev":
    UPLOAD_FOLDER = 'C:/Users/novneet.patnaik/Documents/GitHub/ML-Analysis-azure/ml_ocr/tmp/upload_files'
elif ENV == "qa":
    UPLOAD_FOLDER = './flaskr/tmp/upload_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'ppt', 'docx', 'mp4', }
# ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    jwt = JWTManager(app)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Add Blueprints
    app = add_blueprints(app)
    # Session(app)
    return app


def add_blueprints(app):
    # Add Blueprints
    app.register_blueprint(to_video.bp)
    app.register_blueprint(video_tagging.bp)
    app.register_blueprint(library.bp)
    app.register_blueprint(landing_pages.bp)

    return app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    """
    This function accepts uploaded file requests and sends back the no of pages of the file
    :input: File/Files
    :return: no of pages of a file or of each file
    """
    f = request.files.get("file")
    filename_list = []
    counter = 0
    # for f in file_list:
    if f.filename != "" and allowed_file(f.filename):
        if " " in f.filename:
            f.filename = f.filename.replace(" ", "_")
        filename_list.append(f.filename)

        # count the number of files
        counter = counter + 1

        # Get AWS Credentials from MongoDB
        data = db['aws_creds'].find_one()
        s3_bucket = 'effyai'
        s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-2',
            aws_access_key_id=data['aws_access_key_id'],
            aws_secret_access_key=data['aws_secret_access_key']
        )

        # Save file in the temporary folder
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_content = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
        s3.Bucket(s3_bucket).put_object(Key=filename, Body=file_content)

        content = {'FILE STATUS': 'SAVED'}
        return content, status.HTTP_200_OK

    else:
        content = {'FILE STATUS': 'NOT SAVED'}
        return content, status.HTTP_500_INTERNAL_SERVER_ERROR


app = create_app()

