from flask import Flask, request
from csrf.csrf import CSRF
from controllers.index import get as get_index
from controllers.login import get as get_login
from controllers.logout import get as get_logout
from controllers.logged_in import get as get_logged_in


app = Flask(__name__)
csrf = CSRF(app)


@app.before_request
def log_request_info():
    app.logger.debug(
        '%s %s%s\n%s',
        request.method,
        request.path,
        '?{}'.format(request.query_string) if request.query_string else '',
        str(request.headers).rstrip()
    )


@app.route('/')
def index():
    return get_index()


@app.route('/login')
def login():
    return get_login(app)


@app.route('/logout')
def logout():
    return get_logout()


@app.route('/logged-in')
def logged_in():
    return get_logged_in(app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
