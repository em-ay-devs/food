import os
from dotenv import load_dotenv
from src.flaskr import create_app

load_dotenv(dotenv_path=os.path.abspath('src/configs/.env'))


def main(setup=False):
    app = create_app()
    return app


if __name__ == '__main__':
    flask_app = main()
    flask_app.run(debug=False, host='0.0.0.0', port=5000)
