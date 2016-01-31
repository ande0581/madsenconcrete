# project/run.py
import os
from project import app

""" when running locally
app.run(debug=True)
"""

# when running on Heroku
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
