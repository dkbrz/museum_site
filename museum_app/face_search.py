import os
from annoy import AnnoyIndex
from PIL import Image
import numpy as np
import face_recognition
from museum_app.models import FacesPainting, FacesPhoto

photo = AnnoyIndex(128, "angular")
photo.load(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/models/photo.ann")
)

painting = AnnoyIndex(128, "angular")
painting.load(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/models/painting.ann")
)


def search_image(input_file, n=50, which="painting"):
    image = np.array(Image.open(input_file))
    encoding = face_recognition.face_encodings(image, model="large")[0]
    if which == "painting":
        result = painting.get_nns_by_vector(encoding, n=n, search_k=-1, include_distances=False)
    else:
        result = photo.get_nns_by_vector(encoding, n=n, search_k=-1, include_distances=False)
    return result


def get_image_results(input_file, session, n=50, which="painting"):
    result = search_image(input_file, n=n, which=which)
    if which == "painting":
        model = FacesPainting
    else:
        model = FacesPhoto
    return [
        session.query(model).get(i).image.exhibit
        for i in result
    ]
