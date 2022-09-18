from msilib.schema import Error
from flask import request

def check_token(state_cache):
    try:
        token = str(request.headers.get('authorization')).split()[1]
        if state_cache.get(token, "Not Fount") == "Not Fount":
            print("token not found")
        return token
    except IndexError:
        print("IndexError")
