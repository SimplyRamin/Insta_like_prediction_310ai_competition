import pandas as pd
import numpy as np
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
