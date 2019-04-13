import os
from flask import abort, Flask, request
from flask_restplus import Api, Resource


module = os.environ.get(
    'FLASK_SETTINGS_MODULE', '{{cookiecutter.lname}}.config')
app = Flask(__name__)
app.config.from_object(module)
api = Api(app)


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
