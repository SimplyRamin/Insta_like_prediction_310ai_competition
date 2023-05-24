import pandas as pd
import numpy as np
import json
from InstagramBot import InstagramBot
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


with open('credentials.json') as f:
    creds = json.load(f)
    login_username = creds['username']
    login_password = creds['password']

ig = InstagramBot(login_username, login_password)
csrf_token, session_id = ig.login(verbose=True)
