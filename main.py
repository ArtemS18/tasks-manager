from app.web.config import setup_config
import uvicorn

def main():
    config = setup_config('env/.env')
    uvicorn.run('app.web.app:app', host=config.HOST, port=config.PORT, reload=config.DEBUG)

if __name__ == '__main__':
    main()