import uvicorn

# svc
from teams_context.api_svc.main import app


def main():
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        exit()
    finally:
        ...


if __name__ == "__main__":
    main()
