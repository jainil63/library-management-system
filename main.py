import uvicorn

import backend


def main():
    uvicorn.run(app=backend.app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
