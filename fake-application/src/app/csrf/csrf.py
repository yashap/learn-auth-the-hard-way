from werkzeug.exceptions import BadRequest
from flask import request, after_this_request, g
from uuid import uuid4
from urllib.parse import urlparse
import re


CSRF_COOKIE = 'csrf_token'
CSRF_FORM_FIELD = 'csrf_token'
CSRF_HEADER = 'X-CSRF-Token'
UUID_V4_REGEX = re.compile('^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', re.IGNORECASE)


def get_csrf_token():
    if 'csrf_token' in g:
        return g.csrf_token
    cookie_token = request.cookies.get(CSRF_COOKIE)
    token = cookie_token if cookie_token else str(uuid4())
    g.csrf_token = token
    return token


def set_csrf_token(response, token):
    scheme = urlparse(request.url).scheme
    response.set_cookie(
        key = CSRF_COOKIE,
        value = token,
        httponly = True,
        secure = scheme == 'https'
    )


def is_uuid_v4(s):
    return isinstance(s, str) and bool(UUID_V4_REGEX.fullmatch(s))


class CSRF(object):
    """Enable CSRF protection for a Flask app
    ::
        app = Flask(__name__)
        csrf = CSRF(app)
    Implements the "Double Submit Cookie" style of CSRF protection. Sets the csrf_token cookie in responses. In protected
    requests (by default, POST/PUT/PATCH/DELETE), compares the csrf_token cookie to the token in the page (either the
    ``csrf_token`` form field, or the ``X-CSRF-Token`` header), and ensures they match. Tokens are v4 UUIDs.
    
    To render a token in a template, use ``{{ get_csrf_token() }}``. In forms, include this in a hidden form field. For
    Ajax requests, put this token in an HTML meta tag, then when making Ajax requests, read the token from the meta tag.

    I chose to implement CSRF protection by hand, vs. using a library, purely for learning purposes.
    """

    def __init__(self, app, protect_methods=set(['POST', 'PUT', 'PATCH', 'DELETE'])):
        app.jinja_env.globals['get_csrf_token'] = get_csrf_token
        self.__init_protection(app, protect_methods)

    def __init_protection(self, app, protect_methods):
        @app.before_request
        def protect_requests():
            token = get_csrf_token()
            if request.method in protect_methods:
                self.__validate_token(token)

            @after_this_request
            def set_csrf_token_cookie(response):
                set_csrf_token(response, token)
                return response

    def __validate_token(self, token):
        if not is_uuid_v4(token):
            raise CSRFValidationError('CSRF token was not a uuid v4')
        page_token = self.__get_page_token()
        if token != page_token:
            raise CSRFValidationError('Token in page and header do not match')

    def __get_page_token(self):
        # First, try to get the token out of a header
        token = request.headers.get(CSRF_HEADER)
        # If it wasn't in a header, try to get it out of a form field
        return token if token else request.form.get(CSRF_FORM_FIELD)


class CSRFValidationError(BadRequest):
    description = 'CSRF validation failed'
