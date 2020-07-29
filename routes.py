from api.api import *

def initialize_routes(api):
    api.add_resource(RpiStatusApi, '/api/v1/status')
    api.add_resource(TestApi, '/api/v1/test')