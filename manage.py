# mapistar
from mapistar.app import app

if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.settings")
    app.serve("127.0.0.1", 5000)
