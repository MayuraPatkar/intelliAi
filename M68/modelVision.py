from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import random

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def image_response(image): 
    raw_image = Image.open(image).convert('RGB')
    
    start_sentence = [
        "a photography of",
        "What I can see is",
        "Image of",
        "The picture is about",
        "The image shows that",
        "In this photo,",
        "This picture depicts",
        "From what I perceive,",
        "Breaking down the picture,",
        "Decoding the imagery,",
        "Examining the photograph reveals",
        "Glimpsing at the scene,",
        "Delving into the image,",
        "Exploring the photograph,",
        "Analyzing the visual content,",
        "Interpreting the scene,",
        "In the depicted scenery,",
        "Considering the elements within the photo,",
        "In this visual representation,",
        "A closer look at the picture shows",
    ]
    
    text = random.choice(start_sentence)
    inputs = processor(raw_image, text, return_tensors="pt")
    out = model.generate(
        **inputs,
        max_length=100,
        num_beams=5,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.2
    )
    
    response = processor.decode(out[0], skip_special_tokens=True)
    
    return response
