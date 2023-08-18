# import json
# import requests
# API_URL = "https://api-inference.huggingface.co/models/MaRiOrOsSi/t5-base-finetuned-question-answering"
# headers = {"Authorization": f"Bearer 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"}
# def query(payload):
#     data = json.dumps(payload)
#     response = requests.request("POST", API_URL, headers=headers, data=data)
#     return json.loads(response.content.decode("utf-8"))
# data = query("question: Where does Christian come from? context: Christian is a student of UNISI but he come from Caserta")
# print(data)

from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline

model_name = "./t5-base-finetuned-question-answering"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)


def useT5FinetunedModel(question, context):
    input = f"question: {question} context: {context}"
    encoded_input = tokenizer([input],
                              return_tensors='pt',
                              max_length=512,
                              truncation=True)
    output = model.generate(input_ids=encoded_input.input_ids,
                            attention_mask=encoded_input.attention_mask)
    output = tokenizer.decode(output[0], skip_special_tokens=True)
    return output

if __name__=="__main__":
    context = "There are ten chairs on the outer circle. In the inner ring, there are five yellow chairs, and the periphery is a black chair."
    question = "How many chairs in the inner circle?"
    print(useT5FinetunedModel(question,context))