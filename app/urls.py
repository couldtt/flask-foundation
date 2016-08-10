from app.http.handlers import (
    index,
)

from app.http.controllers import (
    UserController
)

handlers = [
    ('/', 'index', index, 'GET'),
]

controllers = [
    (UserController, '/user'),
]

resources = [

]
