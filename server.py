from fastapi import FastAPI, Form, Cookie
from fastapi.datastructures import Default
from fastapi.responses import Response, JSONResponse

from typing import Optional

import hashlib
import base64

from utils import sign_data, get_username_from_signed_string, PASSWORD_SALT

app = FastAPI()

users = {
    'vitalii': {
        'name': 'vitalii',
        'password': 'bb79b7f2d6f03141c8d905cf763007cb94206a41024b7ba2d642cd90b7813115',  # 'ad'
        'earnings': 10_000
    },
    'ad': {
        'name': 'ad',
        'password': 'bb79b7f2d6f03141c8d905cf763007cb94206a41024b7ba2d642cd90b7813115',  # 'ad'
        'earnings': 20_000
    },
    'admin': {
        'name': 'admin',
        'password': '9214f356360e54afe1271f904b0291e65a1043ad5569dbe1cfa9e7547c9d9e5a',  # 'admin'
        'earnings': 30_000
    },
}


def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash = users.get(username)['password'].lower()
    return password_hash == stored_password_hash


@app.get('/')
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r') as f:
        login_page = f.read()

    if not username:
        return Response(login_page, media_type='text/html')

    valid_username = get_username_from_signed_string(username)

    if not valid_username:
        response = Response(login_page, media_type='text/html')
        response.delete_cookie(key='username')
        return response

    try:
        user = users[valid_username]
    except KeyError:
        response = Response(login_page, media_type='text/html')
        response.delete_cookie(key="username")
        return response

    return Response(
        f"Hello, {user['name']}! <br />"
        f"You have {user['earnings']}$ on your account.",
        media_type='text/html')


@app.post('/login')
def login(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)

    if not user or not verify_password(username, password):
        # return Response("User doesn't exist. Try agen!")
        return JSONResponse({
            "success": False,
            "message": "I don't know you!",
        })

    # response = Response(f"Hello {user['name']}! <br /> You have {user['earnings']}$ on your account.",
    #                     media_type='text/html')
    response = JSONResponse({
        "success": True,
        "message": f"Hello {user['name']}! <br /> You have {user['earnings']}$ on your account.",
    })

    username_signed = base64.b64encode(username.encode()).decode() + '.' + sign_data(username)
    response.set_cookie(key="username", value=username_signed)

    return response




