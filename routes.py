from api.api import *

def initialize_routes(api):
    api.add_resource(RpiStatusApi, '/api/v1/status')
    api.add_resource(TestApi, '/api/v1/test')
    api.add_resource(LocationApi, '/api/v1/location')
    api.add_resource(SpeedTestApi, '/api/v1/speedTest')
    api.add_resource(FlightScheduleApi, '/api/v1/flightSchedule/<id>/<status_code>')