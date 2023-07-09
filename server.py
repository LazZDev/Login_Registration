from flask_app import app

# Import the controllers module
from flask_app.controllers import users

# Run the Flask application if this file is the main entry point
if __name__ == "__main__":
    # Start the Flask application in debug mode
    app.run(debug=True)
