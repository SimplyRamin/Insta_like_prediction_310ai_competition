# resource for making the api: https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f

# to send image to the api, this procedure might be the best. create a client app to run and send the image to the deployed api, the image can be send as string and decode it on the server.
# useful resource: https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

import pandas as pd
import numpy as np
import json
from InstagramBot import InstagramBot
from flask import Flask
from flask_restful import Resource, Api, reqparse
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box


ramin_theme = Theme({
    'success': 'italic bright_green',
    'error': 'bold red',
    'progress': 'italic yellow',
    'header': 'bold cyan',
})
console = Console(theme=ramin_theme)
app = Flask(__name__)
api = Api(app)

# uncomment these lines to test the login procedure.
# with open('credentials.json') as f:
#     creds = json.load(f)
#     login_username = creds['username']
#     login_password = creds['password']

# ig = InstagramBot(login_username, login_password)
# csrf_token, session_id = ig.login()

class Predict(Resource):
    ...


api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run()
