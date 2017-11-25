#!flask/bin/python

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()



files = [
    {
        'id': 1,
        'name': u'Cool',
        'file_summary': u'Cool',
        'content': u'Yes, very cool'
    },
    {
        'id': 2,
        'name': u'test.txt',
        'file_summary': u'testing this system!!!',
        'content': u'Here is where all the content will be sorted'
    }
]

file_fields = {
    'name': fields.String,
    'file_summary': fields.String,
    'uri': fields.Url('f')
}

f_fields = {
        'name' : fields.String,
        'file_summary' : fields.String,
        'content' : fields.String, 
        'uri' : fields.Url('files')
}



class FileListAPI(Resource):
#     decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
                                    'name', type=str,
                                    required=True,
                                    help='No f name provided',
                                    location='json'
                                    )
        self.reqparse.add_argument(
                                    'file_summary', type=str,
                                    default="",
                                    location='json'
                                    )
        self.reqparse.add_argument(
                                    'content', type=str,
                                    default="",
                                    location='json'
                                    )
        super(FileListAPI, self).__init__()

    def get(self):
        return {'files': [marshal(f, f_fields) for f in files]}

    def post(self):
        args = self.reqparse.parse_args()
        f = {
            'id': files[-1]['id'] + 1,
            'name': args['name'],
            'file_summary': args['file_summary'],
            'content': args['content']
        }
        files.append(f)
        return {'f': marshal(f, f_fields)}, 201


class FileAPI(Resource):
#     decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
                                    'name', type=str,
                                    required=True,
                                    location='json'
        )
        self.reqparse.add_argument(
                                    'file_summary', type=str,
                                    location='json'
        )
        self.reqparse.add_argument(
                                    'content', type=str, 
                                    location='json'
        )
        super(FileAPI, self).__init__()

    def get(self, id):
        f = [f for f in files if f['id'] == id]
        if len(f) == 0:
            abort(404)
        return {'f': marshal(f[0], f_fields)}

    def put(self, id):
        f = [f for f in files if f['id'] == id]
        if len(f) == 0:
            abort(404)
        f = f[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                f[k] = v
        return {'f': marshal(f, file_fields)}

    def delete(self, id):
        f = [f for f in files if f['id'] == id]
        if len(f) == 0:
            abort(404)
        files.remove(f[0])
        return {'result': True}


api.add_resource(FileListAPI, '/files', endpoint='files')
api.add_resource(FileAPI, '/file/<int:id>', endpoint='file')


if __name__ == '__main__':
    app.run(debug=True)



