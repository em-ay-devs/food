import os
import argparse
from dotenv import load_dotenv
from src.flaskr import create_app

load_dotenv(dotenv_path=os.path.abspath('src/configs/.env'))


def main(setup=False):
    app = create_app()
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='em-ay-devs-food',
        usage='app.py [options]',
        description='Start food server'
    )
    parser.add_argument('-d', '--dev', action='store_true', help='enable development server mode')
    args = parser.parse_args()
    flask_app = main()
    flask_app.run(debug=args.dev, host='0.0.0.0', port=5000)
