import threading 

_localdata = threading.local()
class Middleware:
    """
    Put the user into current thread local data
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        _localdata.loginuser = request.user

        response = self.get_response(request)


        return response

def get():
    try:
        return _localdata.loginuser
    except:
        return None

