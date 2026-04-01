from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN_KEY = os.getenv("TOKEN_KEY")
ALGO = os.getenv("ALGO")

def lazy(auth):
    token = auth.split()[1]
    user = jwt.decode(token, TOKEN_KEY, ALGO)
    return user

def check_pwd(pwd):
    if len(pwd) >= 10 and any(c.islower() for c in pwd) and any(c.isupper() for c in pwd) and any(c.isdigit() for c in pwd):
        return True
    else:
        return False