# mapistar
import os
from mapistar.app import app

if __name__ == "__main__":
    app.serve("127.0.0.1", 5000)
