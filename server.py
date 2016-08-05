from app import create_app
from app.config import config

app = create_app(config)

@app.route('/')
def main():
    return 'main page'

if __name__ == '__main__':
    app.run(debug=True)