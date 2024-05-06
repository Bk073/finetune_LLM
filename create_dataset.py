import requests
import ast
import json
import pandas as pd
import time

def get_documents_list():
  headers = {
        'Authorization': 'Bearer dataset-TuduFzm4qDck63ZbsvPSGB5b',
        'Content-Type': 'application/json'
    }
  response = requests.get('https://dify.cht77.com/v1/datasets/1c8eb734-62fb-46c3-bd72-b7add31d29d0/documents', headers=headers)
  response = response.content.decode('utf-8').replace("'", '"')
  response = json.loads(response)
  return response['data']

def get_context(id_=None):
  headers = {
      'Authorization': 'Bearer dataset-TuduFzm4qDck63ZbsvPSGB5b',
      'Content-Type': 'application/json'
  }
  # response = requests.get('https://dify.cht77.com/v1/datasets/a7d7b96b-c53b-4a70-884a-36fa61045ea9/documents/be58bcc6-6243-44cb-a707-929379c9db4d/segments', headers=headers)
  path_ = 'https://dify.cht77.com/v1/datasets/1c8eb734-62fb-46c3-bd72-b7add31d29d0/documents/'+id_+'/segments'
  response = requests.get(path_, headers=headers)
  response = response.content.decode('utf-8').replace("'", '"')
  response = json.loads(response)
  return response['data']

def convert_response(response):
  token_list = []
  for i in response.split('\n'):
    try:
      token_list.append(json.loads(i)['response'])
    except:
      continue
  sentence = ''.join(token for token in token_list)
  return sentence

def generate_question_answer(context, model='llama2'):
  '''
  here the prompt given the to model could also be changed in future based on the results
  '''
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  prompt = f"""#content: {context}. Based on the content create two factual question and two abstractive question and answer of each question.
   Do not add answer based on your past knowledge. Return in the following format, 'don't change the format and just response question and answer no other text':
  Do not add : Sure, I can help you with that! Here are two factual and two abstractive questions and answers based on the content of the provided search result page:\n\n
  or any other text: 
  
   ##Factual Question:
   ##Factual Answer:

   ##Abstractive Question:
   ##Abstractive Answer:

   ##Factual Question:
   ##Factual Answer:

   ##Abstractive Question:
   ##Abstractive Answer: """

  data = {"model": model,"prompt":prompt, "keep_alive": "10m"}
  response = ''
  while response == '':
    try:
        response = requests.post('https://my.cht77.com/oapi-rtx/api/generate', headers=headers, data=json.dumps(data))
        response = response.content.decode('utf-8').replace("'", '"')
        break
    except:
        time.sleep(10)
        continue
  return convert_response(response)


def main():
  doc_list = get_documents_list()
  dataset = {}
  dataset['context'] = []
  dataset['question'] = []
  dataset['answer'] = []
  for doc in doc_list:
    splits = get_context(doc['id'])
    for context in splits:
      response = generate_question_answer(context['content'])
      pairs = response.split('##')
      for i in range(len(pairs)):
        words = pairs[i].split()
        if 'Question:' in words:
          question = pairs[i].split("Question:")[-1]
          dataset['question'].append(question)
        elif 'Answer:' in words:
          answer = pairs[i].split("Answer:")[-1]
          dataset['answer'].append(answer)
        else:
          dataset['context'].extend([context['content']]*4)
      
  return dataset

if __name__ == '__main__':
    dataset = main()
    df = pd.DataFrame.from_dict(dataset)
    df.to_csv('data.csv')