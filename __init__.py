from app import app
from config import config

if __name__ == '__main__':
    print(config["pin"])
    app.run(debug=True)