class Response:

    @classmethod
    def success(cls):
        return {'msg': 'success', 'description': '请求成功'}