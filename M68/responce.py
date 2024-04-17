from M68.modelVision import image_response
from M68.inference import inference


def responce(promt = None, image=None):
    print("promt: ",promt, "image: ",image)
    if image:
        return image_response(image)
    else:
        responce = inference(promt)

    return responce
