from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import random

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


def image_response(image): 
    raw_image = Image.open(image).convert('RGB')
    start_sentence = ["a photography of", "What i can see is", "Image of", "THe picture is about", "The image shows that"]
    text = random.choice(start_sentence)
    inputs = processor(raw_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    response = processor.decode(out[0], skip_special_tokens=True)

    return response
