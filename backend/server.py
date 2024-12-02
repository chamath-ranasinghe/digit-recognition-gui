import flask
import base64
from io import BytesIO
from digit_rec import predict_digit
from PIL import Image
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def mainRoute():
    return("Working");

@app.route("/run", methods=["POST"])
def predictDigit():
    # Get the base64-encoded image data from the request
    data = flask.request.get_json()
    image_data = data.get('image')
    
    # Decode the base64 string into bytes
    image_data = image_data.split(",")[1]  # Remove the prefix ("data:image/png;base64,")
    image_bytes = base64.b64decode(image_data)
    
    # Create an image from the bytes
    image = Image.open(BytesIO(image_bytes))
    # Save the image to a file
    #image.save("uploaded_image.png")

    digit,acc = predict_digit(image);
    
    return flask.jsonify({"Prediction": f"{digit}"})







app.run(port=8080, debug=True)