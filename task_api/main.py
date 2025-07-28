from app.web.config import setup_config
import uvicorn


def main():
    config = setup_config()
    uvicorn.run(
        "app.web.app:setup_app",
        host=config.web.host,
        port=config.web.port,
        reload=config.web.reload,
        workers=config.web.workers,
    )


if __name__ == "__main__":
    main()
