import json
import threading
import time

from flask import Flask, request
from flask_restx import Resource, fields, Api

from werkzeug.datastructures import FileStorage
from werkzeug.utils import  secure_filename

ALLOWED_EXTENSIONS = ["txt", "md"]
ALLOWED_MIME_TYPES = ["text/plain"] #['image/png', 'image/jpeg', 'application/pdf']

app = Flask(__name__)
api = Api(app)

app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024  # 0.5 megabytes

model = api.model("Model", {
    "name": fields.String,
    "address": fields.String,
    "email": fields.String,
    # 'date_updated': fields.DateTime(dt_format='rfc822'),
})

upload_parser = api.parser()

upload_parser.add_argument("file", location="files", type=FileStorage, required=True)
upload_parser.add_argument("body", location="form",  default={"name":"pete letkeman", "address":"803-1100 King St. W.\nToronto Ontario\nCanada\nM6K 0C6\n519.331.1405\npete@letkeman", "email":"pete@letkeman.ca"})

def make_llm_request():
    print("Thread started")
    with open("sample.txt", "w+t", encoding="utf-8") as t:
        for i in range(10):
            t.write(str(i))
            time.sleep(3)  # Simulate some work being done
    print("Thread finished")



def allowed_file(filename) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route("/upload/")
@api.expect(upload_parser)
class Upload(Resource):

    def do_something_with_file(self, uploaded_file):
        print(uploaded_file)
        return "ss"

    def post(self):

        # Create a new thread that runs the function do_this()
        thread = threading.Thread(target=make_llm_request)

        # Start the thread
        thread.start()


        args = upload_parser.parse_args()
        uploaded_file = args["file"]  # This is FileStorage instance
        url = self.do_something_with_file(uploaded_file)
        form_data = request.form.to_dict()
        json_body = json.loads(form_data["body"])
        filename = secure_filename(uploaded_file.filename)
        if allowed_file(filename):
            if str(uploaded_file).endswith("('text/plain')>"):
                uploaded_file.save(filename)
        # print(uploaded_file.stream)
        print("data")
        print(json_body["name"])

        return {"url": url}, 201

@api.route("/todo")
class Todo(Resource):
    @api.marshal_with(model, envelope="resource")
    def get(self, **kwargs):
        return model # Some function that queries the db


if __name__ == "__main__":
    app.run(debug=True)
