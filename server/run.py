from app import app


import logging


logging.getLogger().setLevel(logging.DEBUG)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
