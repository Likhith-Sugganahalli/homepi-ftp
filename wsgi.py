
"""Application entry point."""
from app import init_app as ftpapp

app = ftpapp()

if __name__ == "__main__":
    app.run(host="0.0.0.0")