from os import getenv
import hmac
import hashlib
def make_hmac(token: str) -> str:
    return hmac.new(getenv("SECRET_KEY", "").encode('utf-8'), token.encode('utf-8'), hashlib.sha256).hexdigest()
