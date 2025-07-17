from flask import Flask, render_template, request, redirect, url_for, session
from ftp_server import login_clear

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ftp_host = request.form.get('ftp_ip')
        ftp_user = request.form.get('ftp_username')
        ftp_pass = request.form.get('ftp_password')

        result = login_clear(ftp_host, ftp_user, ftp_pass)

        if result['success']:
            session['ftp_info'] = {
                'host': ftp_host,
                'username': ftp_user,
                'password': ftp_pass,
                'file_list': result['file_list']
            }
            session['files'] = result['file_name_list']
            session['current_dir'] = result['current_dir']

            return redirect(url_for('index'))
        else:
            return render_template('login.html', error=result['error'])

    return render_template('login.html')


@app.route('/index')
def index():
    ftp_info = session.get('ftp_info')
    files = session.get('files')
    current_dir = session.get('current_dir')
    file_list = ftp_info.get('file_list') if ftp_info else []

    if not ftp_info:
        return redirect(url_for('login'))

    return render_template('index.html',
                           files=files,
                           ftp_info=ftp_info,
                           current_dir=current_dir,
                           file_list=file_list)


if __name__ == '__main__':
    app.run(debug=True)
