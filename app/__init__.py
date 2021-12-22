from flask import Flask, render_template, request, session, send_file
from pytube import YouTube
from io import BytesIO
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mbleina'

bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
	message = None
	url = None
	if request.method == 'POST':
		session['link'] = request.form.get('url')
		try:
			url = YouTube(session['link'])
			url.check_availability()
		except Exception as e:
			print(e)
			message = 'Video does not seem to exist. Please check your link and try again'
	return render_template('home.html', message=message, url=url)

@app.route('/download',methods=['POST'])
def download_video():
	buffer = BytesIO()
	url = YouTube(session['link'])  
	itag = int(request.form.get('itag'))
	print(itag)
	video = url.streams.get_by_itag(itag)
	video.stream_to_buffer(buffer)
	buffer.seek(0)
	return send_file(buffer, as_attachment=True, download_name='{}.mp4'.format(url.title), mimetype='video/mp4') 