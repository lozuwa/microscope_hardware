import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response, jsonify
from werkzeug import secure_filename
import numpy as np 
# Set cors 
from flask_cors import CORS, cross_origin
# Threads 
import eventlet
eventlet.monkey_patch()

# HTML code to post a file to the server 
html_post_file = ''' 
<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"
          rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h3 class="text-muted">How To Upload a File</h3>
      </div>
      <hr/>
      <div>
      
      <form action="post_image" method="post" enctype="multipart/form-data">
        <input type="file" name="file"><br /><br />
        <input type="submit" value="Upload">
      </form>
      </div>
    </div>
  </body>
</html>
'''

html_post_message = ''' 
<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"
          rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h3 class="text-muted">Send a message</h3>
      </div>
      <hr/>
      <div>

      <form action="post_message" method="post">
        <input type="text" name="sent_message"><br /><br />
        <input type="submit" value="Send">
      </form>
      </div>
    </div>
  </body>
</html>
'''

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'C:/Users/HP/Documents/Research/CLICK/Hardware/images/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Main page for the webpage 
@app.route('/', methods=['GET'])
def index():
	return '''<b> Welcome to the home page </b>'''

# This route will show a form to perform an AJAX request jQuery is loaded to execute the request and update the vars(object)lue of the operation
@app.route('/post_image', methods=['GET'])
def image():
	if request.method == 'GET':
		#return render_template('index.html')
		return html_post_file
	else:
		return ''' Not supported method '''

# Route that will post a message
@app.route('/post_message', methods=['POST', 'GET'])
def post():
	if request.method == 'GET':
		return html_post_message
	elif request.method == 'POST':
		requested = request.form['sent_message']
		print( str(requested) )
		return jsonify({'result': 'success'})
	else:
		return ''' <b> Welcome to the message page </b> '''

# Route that will process the file upload
@app.route('/post_image', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		# Get the name of the uploaded file
		file = request.files['file']
		print(file)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#return redirect(url_for('uploaded_file', filename=filename))
			return jsonify({'result': 'success'})
	else:
		return '''<b> GET method not supported </b>'''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/get_cam_state', methods=['GET'])
def get_cam_state():
	if request.method == 'GET':
		return jsonify({'result': str(state)})

def listen():
	global state
	while True:
		state = int(np.random.rand()*10)
		print(state)
		eventlet.sleep(0.5)

eventlet.spawn(listen)

if __name__ == '__main__':
	app.run(host="192.168.3.213",
			port=int("5000"),
			debug=True)
