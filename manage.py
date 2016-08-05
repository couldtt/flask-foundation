from app import create_app, db
from app.config import config

from flask_script import (
    Server,
    Shell,
    Manager,
    prompt_bool,
)


def _make_context():
    return {
        'app' : create_app(config),
        'db': db,
    }


app = create_app(config)
manager = Manager(app)


@manager.command
def test():
    return 'test'
