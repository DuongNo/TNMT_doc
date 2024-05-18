from app.config import settings

HTTP_CODE = {
    '200': {
        'status_code': 200,
        'message': 'Success'
    },
    '201': {
        'status_code': 201,
        'message': 'Created'
    },
    '400': {
        'status_code': 400,
        'message': 'Bad request'
    },
    '401': {
        'status_code': 401,
        'message': 'Unauthorized'
    },
    '403': {
        'status_code': 403,
        'message': 'Forbidden'
    },
    '404': {
        'status_code': 404,
        'message': 'Not found'
    },
    '408': {
        'status_code': 408,
        'message': 'Request timeout'
    },
    '500': {
        'status_code': 500,
        'message': 'Internal server error'
    },
    '502': {
        'status_code': 502,
        'message': 'Bad gateway'
    }
}


class ResponseFormat:
    def __init__(self):
        self.name = settings.PROJECT_NAME

    @staticmethod
    def success(data: any, message: str = None):
        return {'status_code': HTTP_CODE['200']['status_code'], 'data': data, "message": message}

    @staticmethod
    def created(data: any):
        return {'status_code': HTTP_CODE['201']['status_code'], 'data': data}

    @staticmethod
    def failed(message=None):
        msg = message if message is not None else HTTP_CODE['500']['message']
        return {'status_code': HTTP_CODE['500']['status_code'], 'message': msg}

    @staticmethod
    def unauthorized(message=None):
        msg = message if message is not None else HTTP_CODE['401']['message']
        return {'status_code': HTTP_CODE['401']['status_code'], 'message': msg}
