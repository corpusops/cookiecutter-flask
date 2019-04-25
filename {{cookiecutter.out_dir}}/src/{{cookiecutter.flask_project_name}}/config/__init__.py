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
    'POSTGRES_DB': 'osm',
    'POSTGRES_USER': 'osm',
    'POSTGRES_PASSWORD': 'osm',
    # Internal projection SRID
    # Shoul be metric projection
    'SRID': 2154,
    'SECRET_KEY': 'supercret',
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


try:
    from .local import *  # noqa
except ImportError:
    pass
