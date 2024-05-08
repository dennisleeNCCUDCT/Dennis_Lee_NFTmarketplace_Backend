from flask import Flask
from app import create_app

app = create_app()

@app.route('/api/v1/hello')  # Define a route
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
