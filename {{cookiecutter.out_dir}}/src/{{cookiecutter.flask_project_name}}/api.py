import os

import psycopg2
from flask import Flask, abort, request
from flask_restplus import Api, Resource

module = os.environ.get(
    'FLASK_SETTINGS_MODULE', '{{cookiecutter.lname}}.{{cookiecutter.flask_settings}}')
app = Flask(__name__)
app.config.from_object(module)
api = Api(app)


def dbconn():
    return psycopg2.connect(
        host=app.config.get('POSTGRES_HOST'),
        dbname=app.config.get('POSTGRES_DB'),
        user=app.config.get('POSTGRES_USER'),
        password=app.config.get('POSTGRES_PASSWORD')
    )


@api.route('/helloworld')
class HelloWorld(Resource):
    def post(self):
        if not request.is_json:
            abort(415)
        ret = request.get_json()
        ret['helloworld'] = 'Hay'
        return ret


if __name__ == '__main__':
    app.run(debug=True)
