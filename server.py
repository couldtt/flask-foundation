from app import create_app, register_controllers
from app.config import config

app = create_app(config)

if __name__ == '__main__':
    app.run(debug=True)
