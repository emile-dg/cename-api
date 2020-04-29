from sys import argv

from cename import app, db
from cename.utils import prepare_db


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1909)