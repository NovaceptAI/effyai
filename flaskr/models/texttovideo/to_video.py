from flask import Blueprint
# from flask_api import status
from moviepy.editor import *

bp = Blueprint('texttovideo', __name__, url_prefix='/ttv')


# Define function to create video clip
def create_video(txt, duration, fps, size):
    # Define text clip
    txt_clip = TextClip(txt, fontsize=70, color='white')
    # Define video clip
    video_clip = CompositeVideoClip([txt_clip.set_position('center')], size=size)
    # Define final video with audio
    final_clip = CompositeVideoClip([video_clip], size=size).set_duration(duration).set_fps(fps)
    return final_clip


@bp.route('/create_video', methods=('GET', 'POST'))
def create_video_call():
    # Define variables
    txt = "Hello, world!"  # Text to be displayed in video
    duration = 5  # Duration of video in seconds
    fps = 25  # Frames per second
    size = (640, 480)  # Video size in pixels

    # Create video clip
    video_clip = create_video(txt, duration, fps, size)

    # Save video file
    video_clip.write_videofile("output.mp4", codec='libx264', audio_codec='aac')
    content = {'FILE STATUS': 'VIDEO SAVED', "STATUS": 200}
    return content
