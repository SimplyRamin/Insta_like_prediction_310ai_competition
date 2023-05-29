# resource for making the api: https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f

# to send image to the api, this procedure might be the best. create a client app to run and send the image to the deployed api, the image can be send as string and decode it on the server.
# useful resource: https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

import pandas as pd
import numpy as np
import json
import cv2
from InstagramBot import InstagramBot
from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from torchvision import models, transforms
import base64

efficient_net = models.efficientnet_b7(weights=models.EfficientNet_B7_Weights.DEFAULT)
efficient_net.eval()
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[.485, .456, .406],
                         std=[.229, .224, .225])
])
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


class Test(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', required=True)
        parser.add_argument('page', required=True)
        args = parser.parse_args()

        image_encoded = bytes(args['image'], 'utf-8')
        image_encoded = base64.b64decode(image_encoded)
        nparr = np.frombuffer(image_encoded, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return {
            'message': f'Image Recieved, size: {image.shape[1], image.shape[0]}'
        }, 200


api.add_resource(Predict, '/predict')
api.add_resource(Test, '/test')

if __name__ == '__main__':
    app.run()
