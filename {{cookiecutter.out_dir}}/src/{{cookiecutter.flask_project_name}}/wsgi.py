import os

from .api import app as application

# activate Sentry if any
sentry_dsn = os.environ.get('SENTRY_DSN', None)
if sentry_dsn:
    from raven.contrib.flask import Sentry
    # read conf from ENV !
    sentry = Sentry()
    application = sentry.init_app(application)
