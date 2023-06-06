# Instagram Like Prediction @310ai Competition

In this repo, I will try to tackle the competition of @310ai which was posted on 15th April. In the case of acceptance, I will make this repo public and cover an article about it.

The whole process is explained in the Jupyter notebooks. Please have in mind that these notebooks are ordered, so please first read the `1 - Data-CV.ipynb` and then `2 - Modeling V2.0.ipynb`.

## Assets Schematic
```
.
│   .gitignore
│   1 - Data-CV.ipynb
│   2 - Modeling V2.0.ipynb
│   Client.py
│   credentials.json
│   InstagramBot.py
│   README.md
│   requirements.txt
│   Server.py
│
├───Archive
│   ...
│
├───Data
│   │   ilsvrc2012_wordnet_lemmas.txt
│   │   images_object v1.0.csv
│   │   main v3.0.csv
│   │   top_100_follower.txt
│   │   top_100_posts.txt
│   │
│   └───Images
│       ...
│
├───Input
│       ...
│
├───Models
│       efficient_netb7.pth
│       xgb v2.0.json
```


## Installation
Installing this repo is fairly easy, just make sure the libraries in the `Requirements.txt` is installed. Also please make sure the files in the `Data` and `Models` folders are present. schematic of the downloaded repo must fit the schematic above.

## Usage
Using this program is fairly simple. First thing please run the `Server.py` in a console and let it run. Please have in mind since in this file we try to Instagram, it might take a little time. After the server ran correctly, now you must run the `Client.py`.

Now please copy the image you want to predict its like amount into the `Input` directory. Now in the `Client.py` console and follow the instructions shown on the screen.

## Considerations
- If you are using this program from places that are geo-restricted (i.e. Iran) access to Instagram, before running the `Server.py` You must connect to a VPN.
- For a better experience, please don't use very high-resolution or large pictures.

----
`@Ramin F.` | [Email](ferdos.ramin@gmail.com) | [LinkedIn](https://www.linkedin.com/in/raminferdos/) | [GitHub](https://github.com/SimplyRamin) | [Personal Portfolio](https://simplyramin.github.io/)