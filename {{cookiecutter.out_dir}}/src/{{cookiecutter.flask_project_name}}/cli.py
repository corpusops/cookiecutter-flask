#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for the {{cookiecutter.lname}} api."""
import sys
import click

from {{cookiecutter.lname}}.api import app


@click.command()
def main(args=None):

    app.run(debug=True)

    """Console script for {{cookiecutter.lname}}."""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.lname}}.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover


# vim:set et sts=4 ts=4 tw=80:
