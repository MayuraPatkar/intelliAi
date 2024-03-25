from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"

# Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def answer(prompt, context):

    QA_input = {
        'question': prompt,
        'context': context,
    }
    res = nlp(QA_input)
    answer_text = res['answer']
    print("response: ", answer_text)
    return answer_text