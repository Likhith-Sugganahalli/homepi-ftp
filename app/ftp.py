import functools

from flask import request, abort, jsonify, redirect, render_template, url_for, send_from_directory, flash, g, current_app,Blueprint
import os
from werkzeug.utils import secure_filename


bp = Blueprint('ftp', __name__, url_prefix='/ftp')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Asked to shutdown')
    func()


def testDirs():
	folder = current_app.config['UPLOAD_DIRECTORY']
	basedir = os.path.abspath(os.path.dirname(__file__))
	upload_dir = os.path.join(basedir,folder)
	print('checking path',upload_dir)
	check = os.path.exists(upload_dir)
	print(check)
	if check:
		return upload_dir
	else:
		
		return None


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def main():
	return('holla')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		upload_dir = testDirs()
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(upload_dir, filename))
			return redirect(url_for('ftp.files_list'))
	return(render_template("upload.html"))

@bp.route('/files')
def files_list():
	upload_dir = testDirs()
	if upload_dir:
		list_of_files = os.listdir(upload_dir)
		return render_template("list_files.html", data=list_of_files)

	else:
		return redirect(url_for('ftp.main'))


@bp.route('/files/<string:filename>')
def uploaded_file(filename):
	upload_dir = testDirs()
	if upload_dir:
		return send_from_directory(upload_dir,filename,as_attachment=True)

	else:
		return redirect(url_for('ftp.main'))


