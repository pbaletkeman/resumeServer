from flask import Flask
from flask_restx import Resource, fields, Api
from werkzeug.datastructures import FileStorage


app = Flask(__name__)
api = Api(app)

model = api.model('Model', {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822'),
})

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@api.route('/upload/')
@api.expect(upload_parser)
class Upload(Resource):

    def do_something_with_file(self, uploaded_file):
        print(uploaded_file)
        return "ss"

    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        url = self.do_something_with_file(uploaded_file)
        uploaded_file.save(uploaded_file.filename )
        print(uploaded_file.stream)
        return {'url': url}, 201

@api.route('/todo')
class Todo(Resource):
    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return model # Some function that queries the db


if __name__ == '__main__':
    app.run(debug=True)
