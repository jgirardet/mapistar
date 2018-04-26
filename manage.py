# Standard Libraries
import os

# mapistar
from mapistar.app import app

if __name__ == "__main__":
    app.serve("127.0.0.1", 5000, debug=True)
