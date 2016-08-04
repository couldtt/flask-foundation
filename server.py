from app import create_app

app = create_app()

@app.route('/')
def main():
    return 'main page'

if __name__ == '__main__':
    app.run(debug=True)