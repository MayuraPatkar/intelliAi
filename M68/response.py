import random
import json
from pathlib import Path
import os
import torch

from M68.model import NeuralNet
from M68.preprocess import bag_of_words, tokenize

BASE_DIR = Path(__file__).resolve().parent.parent

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open(os.path.join(BASE_DIR, "M68\\intents.json"), 'r', encoding='utf-8') as f:
    intents = json.load(f)

FILE = os.path.join(BASE_DIR, "M68\\data.pth")
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def responce(promt):

    sentence = tokenize(promt)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                responce = random.choice(intent['responses'])
    else:
        responce =" I do not understand..."

    return responce