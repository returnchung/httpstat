import os
from httpstat import app

if __name__ == "__main__":
    app.config["ENV"] = "development"
    app.config["DEBUG"] = True
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 32767))
