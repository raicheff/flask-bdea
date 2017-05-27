#
# Flask-Keen
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import warnings


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
        project_id = app.config.get('KEEN_PROJECT_ID')
        if project_id is None:
            warnings.warn('KEEN_PROJECT_ID not set', RuntimeWarning, stacklevel=2)
            return
        self.client = KeenClient(
            project_id=project_id,
            write_key=app.config.get('KEEN_WRITE_KEY'),
            read_key=app.config.get('KEEN_READ_KEY'),
        )

    def __getattr__(self, name):
        return getattr(self.client, name)


# EOF
