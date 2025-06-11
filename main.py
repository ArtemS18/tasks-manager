from app.web.app import setup_app
from uvicorn import run

from app.web.config import setup_config

def main():
    config = setup_config('env/.env')
    app = setup_app()
    run(app, host=config.HOST, port=config.PORT)

if __name__ == '__main__':
    main()