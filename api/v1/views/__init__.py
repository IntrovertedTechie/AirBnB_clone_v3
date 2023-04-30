from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)

# Register the app_views blueprint with a trailing slash in the URL prefix
app.register_blueprint(app_views, url_prefix='/api/v1/')

if __name__ == '__main__':
    app.run()
