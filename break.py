 
 #!/usr/bin/env python3

import guestfs
import sys

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

class Break(Resource):
    def post(self):
        input = request.get_json()
        g = guestfs.GuestFS(python_return_dict=True)
        g.set_backend("direct")
        g.add_drive_opts("", protocol="nbd", format="raw", server=["unix:%s" % sys.argv[1]], readonly=1)
        g.launch()
        return jsonify(vm_config)

def main():
    print("Socket: %s" % sys.argv[1])
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Break, '/break')
    app.run(host= '0.0.0.0')


if __name__ == '__main__':
    main()
