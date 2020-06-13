# This is a top-level script that defines which flask app you want to run
from app_package import app

import sys
import os

if __name__ == '__main__':
        host = os.environ.get('HOST', '0.0.0.0')
        app.run(host=host)