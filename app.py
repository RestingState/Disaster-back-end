from app import api
from wsgiref.simple_server import make_server
from app.rest.api import api_blueprint
from app.rest.sky_info_api import sky_blueprint


api.register_blueprint(api_blueprint)
api.register_blueprint(sky_blueprint)

with make_server('', 5000, api) as server:
    server.serve_forever()

# if __name__ == "__main__":
#     # api.run('0.0.0.0')
#     # serve(api, port=5000)
#     api.run(debug=True, port=5000)
