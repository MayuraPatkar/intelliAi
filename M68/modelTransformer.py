from transformers import pipeline

generator = pipeline('text-generation', model='gpt2-medium')

def context(prompt):
    output_text = generator(prompt, max_length=300)
    generated_text = output_text[0]['generated_text']
    print("context: ", generated_text)
    return generated_text