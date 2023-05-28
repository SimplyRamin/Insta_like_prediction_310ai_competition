# Client script for making the image into string and send it via post method to the api.

import requests
import cv2
from os import path
from rich.console import Console
from rich.theme import Theme
import json
ramin_theme = Theme({
    'success': 'italic bright_green',
    'error': 'bold red',
    'progress': 'italic yellow',
    'header': 'bold cyan',
})
console = Console(theme=ramin_theme)


api_address = 'http://localhost:5000/test'
input_address = 'Input/'
content_type = 'application/json'
headers = {'content-type': content_type}

console.print('Welcome to the Instagram like predictor client, Designed by [header]Ramin F. for @310.ai Competition[/].')
console.print('Please copy the image you want to process into the Input folder and type the name of it plus its format:')
console.print('for example: image1.jpg')
image_name = input('>')
if path.isfile(f'{input_address}{image_name}'):
    image = cv2.imread(f'{input_address}{image_name}')
    image_format = '.' + image_name.split('.')[1]
    _, image_encoded = cv2.imencode(image_format, image)
    console.print('Image read.', style='success')
else:
    console.print(f'{image_name} not found!', style='error')
    console.print('Rerun the program.', style='progress')
    exit()

console.print('Please enter the name of profile that this image will be published in.')
console.print('for example: natgeo')
page = input('>')
response = requests.post(api_address, json={'image': str(image_encoded.tobytes()),
                                            'page': str(page)}, headers=headers)

console.print(json.loads(response.text))