from app import api
from wsgiref.simple_server import make_server
from app.rest.test_api import api_blueprint


api.register_blueprint(api_blueprint)
with make_server('', 5000, api) as server:
    server.serve_forever()

# if __name__ == "__main__":
#     # api.run('0.0.0.0')
#     # serve(api, port=5000)
#     api.run(debug=True, port=5000)
