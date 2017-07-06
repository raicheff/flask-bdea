#
# Flask-Keen
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import re
import warnings

from bdea.client import BDEAClient
from flask import current_app

try:
    from wtforms.validators import ValidationError
except ImportError:
    pass


domain_re = re.compile('^(\S+)@(\S+)')


class BDEA(object):
    """
    Flask-BDEA

    Documentation:
    https://flask-bdea.readthedocs.io

    :param app: Flask app to initialize with. Defaults to `None`
    """

    client = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        api_key = app.config.get('BDEA_API_KEY')
        if api_key is None:
            warnings.warn('BDEA_API_KEY not set', RuntimeWarning, stacklevel=2)
            return
        self.client = BDEAClient(api_key)
        app.extensions['bdea'] = self

    def __getattr__(self, name):
        return getattr(self.client, name)


class NonDisposableEmail(object):
    """
    Validates an email address.

    :param message:
        Error message to raise in case of a validation error.
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):

        if current_app.debug:
            return

        message = self.message or field.gettext('Unacceptable email address.')

        match = domain_re.match(field.data.strip().lower())
        if match is None:
            raise ValidationError(message)

        is_disposable = current_app.extensions['bdea'].get_domain_status(match.group(2)).is_disposable()
        if is_disposable:
            message = self.message
            if message is None:
                message = field.gettext('Unacceptable email address.')
            raise ValidationError(message)


# EOF
