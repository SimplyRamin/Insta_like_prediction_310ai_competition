# resource for making the api: https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f

# to send image to the api, this procedure might be the best. create a client app to run and send the image to the deployed api, the image can be send as string and decode it on the server.
# useful resource: https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

import numpy as np
import base64
import json
import cv2
from InstagramBot import InstagramBot
from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
import torch
from torchvision import models, transforms
import xgboost as xgb

efficient_net = models.efficientnet_b7(weights=models.EfficientNet_B7_Weights.DEFAULT)
efficient_net.eval()
model = xgb.XGBRegressor()
model.load_model('Models/xgb v2.0.json')
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[.485, .456, .406],
                         std=[.229, .224, .225])
])
with open('Data/ilsvrc2012_wordnet_lemmas.txt', 'r') as f:
    categories = [s.strip() for s in f.readlines()]
app = Flask(__name__)
api = Api(app)

# uncomment these lines to test the login procedure.
with open('credentials.json') as f:
    creds = json.load(f)
    login_username = creds['username']
    login_password = creds['password']

ig = InstagramBot(login_username, login_password)
csrf_token, session_id = ig.login()


class Predict(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', required=True)
        parser.add_argument('page', required=True)
        parser.add_argument('post_type', required=True)
        args = parser.parse_args()

        # Image object detection part
        image_encoded = bytes(args['image'], 'utf-8')
        image_encoded = base64.b64decode(image_encoded)
        nparr = np.frombuffer(image_encoded, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_tensor = transform(image_rgb)
        input_batch = input_tensor.unsqueeze(0)
        with torch.no_grad():
            output = efficient_net(input_batch)
        detected_object = torch.nn.functional.softmax(output[0], dim=0)
        prob, cat = torch.topk(detected_object, 1)

        # Extracting other features for the prediciton from the Instagram
        features_dict = ig.load(args['page'], csrf_token, session_id)
        prediction_input_lst = [
            'GraphSideCar' if args['post_type'] == 'carousel' else 'GraphImage',
            features_dict['category'],
            features_dict['follower'],
            features_dict['following'],
            features_dict['ar_effect'],
            features_dict['type_business'],
            features_dict['type_professional'],
            features_dict['verified'],
            features_dict['reel_count'],
            features_dict['reel_view_mean'],
            features_dict['reel_comment_mean'],
            features_dict['reel_like_mean'],
            features_dict['reel_duration_mean'],
            features_dict['reel_frequency'],
            features_dict['media_count'],
            features_dict['media_comment_mean'],
            features_dict['media_like_mean'],
            features_dict['media_frequency'],
            categories[cat[0]],
        ]
        prediction = model.predict(prediction_input_lst)

        return {
            'message': f'Image Recieved, size: {image.shape[1], image.shape[0]}',
            'object': f'{categories[cat[0]]}',
            'prob': f'{prob[0]:.4f}',
        }, 200


api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run()
