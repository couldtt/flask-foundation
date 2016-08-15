from app import create_app, db
from app.config import config
from app.models import *

from flask_script import (
    Server,
    Shell,
    Manager,
    prompt_bool,
)
from flask_migrate import (
    Migrate,
    MigrateCommand
)


def _make_context():
    return {
        'app': create_app(config),
        'db': db,
    }


app = create_app(config)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server(use_debugger=True, use_reloader=True, host='0.0.0.0'))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    if prompt_bool('Are you sure?'):
        db.drop_all()


@manager.command
def recreate_db():
    drop_db()
    create_db()


if __name__ == '__main__':
    manager.run()
