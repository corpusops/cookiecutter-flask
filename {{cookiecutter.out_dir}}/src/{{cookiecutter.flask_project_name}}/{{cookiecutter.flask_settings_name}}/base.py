#
# Local postgis database with local user as the same name as the data base
#

import os

import six

# Nothing to define in the settings

globs = globals()
DEFAULT_SETTINGS = {
    # Database over a network interface
    'POSTGRES_HOST': 'localhost',
    'POSTGRES_PORT': 5432,
    'POSTGRES_DB': 'db',
    'POSTGRES_USER': 'user',
    'POSTGRES_PASSWORD': 'password',
    # Internal projection SRID
    # Shoul be metric projection
    'SRID': 2154,
    'SECRET_KEY': 'supercret',
{% if cookiecutter.with_celery %}
    # Celery settings
    'CELERY_BROKER_URL': 'amqp://celery-broker//',
{% if 'post' in cookiecutter.db_mode %}
    'CELERY_RESULT_BACKEND': 'db+postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}',
{% else %}
    'CELERY_RESULT_BACKEND': 'rpc://',
{% endif %}
    'CELERY_RESULT_PERSISTENT': True,
    #: Only add pickle to this list if your broker is secured
    #: from unwanted access (see userguide/security.html)
    'CELERY_ACCEPT_CONTENT': ['json'],
    'CELERY_TASK_SERIALIZER': 'json',
{% endif %}
}


def as_col(value, separators=None, final_type=None, **kw):
    if final_type is None:
        final_type = list
    if separators is None:
        separators = ['-|_', '_|-', '___', ',', ';', '|']
    if isinstance(value, six.string_types):
        assert(len(separators))
        while separators:
            try:
                separator = separators.pop(0)
            except IndexError:
                break
            if separator in value:
                break
        value = final_type(value.split(separator))
        if final_type is not list:
            value = final_type(value)
    return value


def as_int(value, **kw):
    if value not in ['', None]:
        if isinstance(value, six.string_types):
            value = value.split()[0].strip()
        value = int(value)
    return value


def as_bool(value, asbool=True):
    if isinstance(value, six.string_types):
        if value and asbool:
            low = value.lower().strip()
            if low in [
                'false', 'non', 'no', 'n', 'off', '0', '',
            ]:
                return False
            if low in [
                'true', 'oui', 'yes', 'y', 'on', '1',
            ]:
                return True
    return bool(value)


# 12 factors settings, defaults to sane values but can be overriden by env
for k, val in six.iteritems(DEFAULT_SETTINGS):
    typ = type(val)
    tfunc = {
        bool: as_bool,
        int: as_int,
        list: as_col,
        set: as_col,
        tuple: as_col,
    }.get(typ, typ)
    globs.update({k: tfunc(os.environ.get(k, val))})

for i in [{%if cookiecutter.with_celery%}"CELERY_RESULT_BACKEND",{%endif%}]:
    try:
        globs[i] = globs[i].format(**globs)
    except KeyError:
        continue


class Celery(object):
    """Celery5 style compatible settings"""
    broker_url = CELERY_BROKER_URL
    result_backend = CELERY_RESULT_BACKEND
    result_persistent = CELERY_RESULT_PERSISTENT
    accept_content = CELERY_ACCEPT_CONTENT
    task_serializer = CELERY_TASK_SERIALIZER

