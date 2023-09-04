from app.app_factory import app
from app.config import PORT, HOST
if __name__ == '__main__':
    app.run(port=PORT, host=HOST, debug=True)
