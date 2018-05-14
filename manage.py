# mapistar
from mapistar.app import app

# from mapistar.db import db

if __name__ == "__main__":
    app.serve("127.0.0.1", 5000, debug=True)
