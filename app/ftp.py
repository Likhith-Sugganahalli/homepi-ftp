import functools

from flask import request, abort, jsonify, redirect, render_template, url_for, send_from_directory, flash, g, current_app,Blueprint,make_response
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
	current_app.logger.info('checking path:{}'.format(upload_dir))
	check = os.path.exists(upload_dir)
	current_app.logger.info(check)
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

'''
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
			print(file.file_size)
			current_app.logger.info(file.file_size)
			filename = secure_filename(file.filename)
			file.save(os.path.join(upload_dir, filename))
			return redirect(url_for('ftp.files_list'))
	return(render_template("upload.html"))
'''

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		upload_dir = testDirs()
		save_path = os.path.join(upload_dir, secure_filename(file.filename))
		current_chunk = int(request.form['dzchunkindex'])

		# If the file already exists it's ok if we are appending to it,
		# but not if it's new file that would overwrite the existing one
		if os.path.exists(save_path) and current_chunk == 0:
			# 400 and 500s will tell dropzone that an error occurred and show an error
			return make_response(('File already exists', 400))

		try:
			with open(save_path, 'ab') as f:
				f.seek(int(request.form['dzchunkbyteoffset']))
				f.write(file.stream.read())
		except OSError:
			# log.exception will include the traceback so we can see what's wrong 
			current_app.logger.exception('Could not write to file')
			return make_response(("Not sure why,"
								  " but we couldn't write the file to disk", 500))

		total_chunks = int(request.form['dztotalchunkcount'])

		if current_chunk + 1 == total_chunks:
			# This was the last chunk, the file should be complete and the size we expect
			if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
				current_app.logger.error(f"File {file.filename} was completed, "
						  f"but has a size mismatch."
						  f"Was {os.path.getsize(save_path)} but we"
						  f" expected {request.form['dztotalfilesize']} ")
				return make_response(('Size mismatch', 500))
			else:
				current_app.logger.info(f'File {file.filename} has been uploaded successfully')
		else:
			current_app.logger.debug(f'Chunk {current_chunk + 1} of {total_chunks} '
					  f'for file {file.filename} complete')

		return make_response(("Chunk upload successful", 200))
	else:
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


