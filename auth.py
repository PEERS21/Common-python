from dotenv import dotenv_values
import hmac
import hashlib
config = dotenv_values("/run/secrets/common_python")
def make_hmac(token: str) -> str:
    return hmac.new(config.get("SECRET_KEY", "").encode('utf-8'), token.encode('utf-8'), hashlib.sha256).hexdigest()
