import requests
import json
from datetime import datetime
import re
from rich.console import Console
from rich.theme import Theme
ramin_theme = Theme({
    'success': 'italic bright_green',
    'error': 'bold red',
    'progress': 'italic yellow',
    'header': 'bold cyan',
})
console = Console(theme=ramin_theme)


class InstagramBot:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.link = 'https://www.instagram.com/accounts/login/'
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                        'referer': 'https://www.instagram.com/',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1',
                        'TE': 'trailers',
                        }

    def login(self, verbose: bool = False):
        """Method for logging into the Instagram to get csrf_token and session_id.

        Args:
            verbose (bool, optional): Key to print extra information. Defaults to False.

        Returns:
            csrf_token: csrf token resulted from logging to the Instagram.
            session_id: session id resulted from logging to the Instagram.
        """
        current_time = int(datetime.now().timestamp())
        response = requests.Session().get(self.link, headers=self.headers)
        if response.ok:
            csrf = re.findall(r'csrf_token\\":\\"(.*?)\\"', response.text)[0]
            payload = {
                'username': self.username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{current_time}:{self.password}',
                'queryParams': {},
                'optIntoOneTap': 'false',
                'stopDeletionNonce': '',
                'trustedDeviceRecords': '{}',
            }

            login_header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrf,
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'X-Instagram-AJAX': 'c6412f1b1b7b',
                'X-IG-App-ID': '936619743392459',
                'X-ASBD-ID': '198387',
                'X-IG-WWW-Claim': '0',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://www.instagram.com',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://www.instagram.com/accounts/login/?',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
            }

            login_response = requests.post(self.login_url, data=payload, headers=login_header)
            json_data = json.loads(login_response.text)

            if json_data['status'] == 'fail':
                console.print(json_data['message'], style='error')
                return json_data['message']

            elif json_data["authenticated"]:
                cookies = login_response.cookies
                cookie_jar = cookies.get_dict()
                csrf_token = cookie_jar['csrftoken']
                session_id = cookie_jar['sessionid']
                if verbose is True:
                    console.print("login successful", style='success')
                    console.print("csrf_token: ", csrf_token, style='progress')
                    console.print("session_id: ", session_id, style='progress')
                return csrf_token, session_id

            else:
                console.print("login failed ", login_response.text, style='error')
                return login_response.headers
        else:
            console.print('error', style='error')
            console.print(response)

    def load(self, page: str, csrf_token: str, session_id: str, verbose: bool = False):
        """Method for loading the account information provided by the user, extracting all the features except the content of the target image for predicting its amount of like.

        Args:
            page (str): Target page that the image will published in.
            csrf_token (str): csrf token that got from the login method.
            session_id (str): session id that got from the login method.
            verbose (bool, optional): Key to print extra information. Defaults to False.

        Returns:
            json: Features except the content of the image to get from the page.
        """
        session = {
            "csrf_token": csrf_token,
            "session_id": session_id
        }

        headers = {
            "x-csrftoken": session['csrf_token'],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Instagram-AJAX': 'c6412f1b1b7b',
            'X-IG-App-ID': '936619743392459',
            'X-ASBD-ID': '198387',
            'X-IG-WWW-Claim': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.instagram.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers'
        }

        cookies = {
            "sessionid": session['session_id'],
            "csrftoken": session['csrf_token']
        }

        url = f'https://www.instagram.com/{page}/?__a=1&__d=dis'
        res = requests.get(url, headers=headers, cookies=cookies)

        if res.status_code == 404:
            console.print(f'Page: {page} is not found!', style='error')
            return res.status_code

        if res.status_code == 200:
            if res.json()['graphql']['user']['is_private'] is True:
                console.print(f'Page: {page} is private!', style='error')
                return 'private'
            else:
                console.print(f'Page: {page} information loaded successfully!', style='success')
                return res.json()
        else:
            console.print(f'Page: {page} information didnt load, returned type: {res.headers["Content-Type"]}', style='error')
            return res.text()
