from api.api import *

def initialize_routes(api):
    api.add_resource(RpiStatusApi, '/api/v2/status')