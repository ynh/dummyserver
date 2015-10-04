from uuid import uuid4
import PIL
from flask import Flask, jsonify
from flask import request, url_for
from PIL import Image
import glob, os
app = Flask(__name__)

dir = os.path.dirname(__file__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            f = request.files['image']
            name = str(uuid4())
            uploads =  os.path.join(dir, 'static/uploads')
            f.save(uploads + '/' +name+'.jpg')
            im = Image.open(uploads+ '/'  +name+'.jpg')
            im.thumbnail((800,800), PIL.Image.ANTIALIAS)
            im.save(uploads+ '/'  +name+'_big.jpg', "JPEG")
            im = Image.open(uploads+ '/'  +name+'.jpg')
            im.thumbnail((128,128), PIL.Image.ANTIALIAS)
            im.save(uploads+ '/'  +name+'_small.jpg', "JPEG")
            # do other stuff with values in request.form
            # and return desired output in JSON format
            return jsonify({'url': 'http://'+request.headers['host']+'/uploads/' +name})
        except Exception as e:
            print(e)

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run()
