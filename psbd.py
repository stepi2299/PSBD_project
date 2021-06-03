from app import app
from database import dbclient


if __name__ == "__main__":
    app.run(debug=True)
    dbclient.connect()
