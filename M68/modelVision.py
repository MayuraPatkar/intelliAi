from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import random

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


def image_response(image): 
    raw_image = Image.open(image).convert('RGB')
    start_sentence = [
        "a photography of",
        "What i can see is",
        "Image of",
        "The picture is about",
        "The image shows that",
        "In this photo,",
        "This picture depicts",
        "From what I perceive,",
        "Observing closely,",
        "It seems to be a snapshot of",
        "Describing the scene,",
        "From my perspective,",
        "Exploring the imagery,",
        "Noticing the details,",
        "Upon examination,",
        "Taking a closer look,",
        "Interpreting the visuals,",
        "Examining the photograph,",
        "Reflecting on the image,",
        "Analyzing the snapshot,",
        "Discussing the composition,",
        "Deciphering the elements,",
        "Identifying the subject,",
        "Breaking down the picture,",
        "Decoding the imagery,",
        "Examining the photograph reveals",
        "Scrutinizing the details,",
        "Glimpsing at the scene,",
        "Upon initial observation,",
        "Pondering the portrayal,",
        "Contemplating the content,",
        "Peering into the picture,",
        "Delving into the image,",
        "Exploring the photograph,",
        "Noting the visual elements,",
        "Scrutinizing the composition,",
        "Analyzing the visual cues,",
        "Pondering over the image,",
        "Reflecting on the snapshot,",
        "Interpreting the scene,",
        "Unraveling the details,",
        "Dissecting the image,",
        "Unpacking the visuals,",
        "Deciphering the scene,",
        "Unveiling the subject,",
        "Delving into the details,",
        "Exploring the scene,",
        "Uncovering the imagery,",
        "Investigating the composition,",
        "Inspecting the elements,",
        "Decoding the composition,",
        "Unraveling the imagery,",
        "Deciphering the composition,",
        "Analyzing the elements,",
        "Breaking down the composition,",
        "Unveiling the content,",
        "Dissecting the snapshot,",
        "Decoding the snapshot,",
        "Unpacking the composition,",
        "Investigating the elements,"
    ]

    text = random.choice(start_sentence)
    inputs = processor(raw_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    response = processor.decode(out[0], skip_special_tokens=True)

    return response
