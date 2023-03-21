# from app import app
import json
import os.path
import boto3
from flask_api import status
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
# from .models import ocr_detect, segmentation_ml, topic_modelling, analysis, summarizer, chronology
from .models.upload_data import get_db, ENV

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


def create_app(test_config=None):
    return app
