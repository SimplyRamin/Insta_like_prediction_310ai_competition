import numpy as np
import pandas as pd
import time
import base64
import json
import cv2
from InstagramBot import InstagramBot
from flask import Flask
from flask_restful import Resource, Api, reqparse
import torch
from torchvision import models, transforms
import xgboost as xgb

efficient_net = torch.load('Models/efficientnetb7.pth')
# If you want to download the model from the scratch, comment the line above and uncomment the line below.
# efficient_net = models.efficientnet_b7(weights=models.EfficientNet_B7_Weights.DEFAULT)
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
login_time = time.time()


class Predict(Resource):
    def post(self):
        request_time = time.time()
        global login_time, csrf_token, session_id
        if (request_time - login_time) / 3600 > 3:
            csrf_token, session_id = ig.login()
            login_time = time.time()
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
        response = ig.load(args['page'], csrf_token, session_id)
        if response['code'] != 200:
            return response
        else:
            prediction_input_df = pd.DataFrame(data=[[
                'GraphSideCar' if args['post_type'] == 'carousel' else 'GraphImage',
                response['features_dict']['category'],
                response['features_dict']['followers'],
                response['features_dict']['following'],
                response['features_dict']['ar_effect'],
                response['features_dict']['type_business'],
                response['features_dict']['type_professional'],
                response['features_dict']['verified'],
                response['features_dict']['reel_count'],
                response['features_dict']['reel_view_mean'],
                response['features_dict']['reel_comment_mean'],
                response['features_dict']['reel_like_mean'],
                response['features_dict']['reel_duration_mean'],
                response['features_dict']['reel_frequency'],
                response['features_dict']['media_count'],
                response['features_dict']['media_comment_mean'],
                response['features_dict']['media_like_mean'],
                response['features_dict']['media_frequency'],
                categories[cat[0]],
            ]], columns=['post_type', 'category_name', 'follower', 'following', 'ar_effect',
                         'type_business', 'type_professional', 'verified', 'reel_count',
                         'reel_avg_view', 'reel_avg_comment', 'reel_avg_like',
                         'reel_avg_duration', 'reel_frequency', 'media_count',
                         'media_avg_comment', 'media_avg_like', 'media_frequency', 'object'])
            prediction_input_df['post_type'] = prediction_input_df['post_type'].astype('category')
            prediction_input_df['category_name'] = prediction_input_df['category_name'].astype('category')
            prediction_input_df['object'] = prediction_input_df['object'].astype('category')
            prediction = model.predict(prediction_input_df)
            return {
                'message': f'Image Recieved, size: {image.shape[1], image.shape[0]}',
                'object': f'{categories[cat[0]]}',
                'prob': f'{prob[0]:.4f}',
                'prediction': f'{prediction[0]},'
            }, 200


class Test(Resource):
    def get(self):
        return {
            'message': 'Hello, World!'
        }


api.add_resource(Predict, '/predict')
api.add_resource(Test, '/test')


if __name__ == '__main__':
    app.run()
