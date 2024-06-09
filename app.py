from flask import Flask, request, render_template, send_from_directory
from PIL import Image, ImageSequence
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
RESULT_FOLDER = 'results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'upload.gif')
    result_image_path = os.path.join(app.config['RESULT_FOLDER'], 'result.gif')
    
    if request.method == 'POST':
        file = request.files.get('file')
        division = int(request.form.get('division', 1))

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'upload.gif')
            file.save(filepath)
            uploaded_image_path = filepath

        if os.path.exists(uploaded_image_path):
            original_image = Image.open(uploaded_image_path)

            # Check if the uploaded image is a GIF
            if original_image.is_animated:
                result_frames = []
                for frame in ImageSequence.Iterator(original_image):
                    small_frame = frame.resize((frame.width // division, frame.height // division), Image.NEAREST)
                    pixel_art_frame = small_frame.resize(frame.size, Image.NEAREST)
                    result_frames.append(pixel_art_frame)
                
                result_frames[0].save(result_image_path, save_all=True, append_images=result_frames[1:], loop=0)
            else:
                small_image = original_image.resize((original_image.width // division, original_image.height // division), Image.NEAREST)
                pixel_art_image = small_image.resize(original_image.size, Image.NEAREST)
                pixel_art_image.save(result_image_path)

    return render_template('index.html', uploaded_image_path=uploaded_image_path, result_image_path=result_image_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
