from dotenv import load_dotenv
from src.flaskr import create_app

load_dotenv()


def main(setup=False):
    app = create_app()
    return app


if __name__ == '__main__':
    flask_app = main()
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
