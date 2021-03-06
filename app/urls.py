from app.http.handlers import (
    index,
)

from app.http.controllers.public import (
    UserController,
    LoginController,
    RegisterController,
)

handlers = [
    ('/', 'index', index, 'GET'),
]

controllers = [
    (UserController, '/user'),
    (LoginController, '/login'),
    (RegisterController, '/register'),
]

resources = [

]
