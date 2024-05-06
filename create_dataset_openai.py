from openai import OpenAI
import os
import pandas as pd
import csv
import requests
import ast
import json
import time 

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

def split_text(file_path, words_per_chunk=200):
  '''
  This method is used to split a file based on the number of words.
  The returned result is the splitted list.
  '''
  with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

  words = text.split()
  chunks = [' '.join(words[i:i+words_per_chunk]) for i in range(0, len(words), words_per_chunk)]
  return chunks

def generate_question_answer(context, model='gpt-4-0125-preview'):
  '''
  here the prompt given the to model could also be changed in future based on the results
  '''
  MODEL = model
  response = client.chat.completions.create(
      model=MODEL,
      messages=[
          {"role": "system", "content":"You are a helpful assistant to create a question and answer. Answer only based on the context. Do not add answer based on your past knowledge"},
          {"role": "user", "content": f"""#content: {context}. Based on the content create two factual question and two abstractive question and answer of each question.
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
            ##Abstractive Answer: """}
        ],
      temperature=0,
  )
  return response.choices[0].message.content

# from own server
def convert_response(response):
  token_list = []
  for i in response.split('\n'):
    try:
      token_list.append(json.loads(i)['response'])
    except:
      continue
  sentence = ''.join(token for token in token_list)
  return sentence

def generate_question_answer_own(context, model='llama2'):
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

def main(file_path):
    dataset = {}
    dataset['context'] = []
    dataset['question'] = []
    dataset['answer'] = []
    splits = split_text(file_path, words_per_chunk=200)
    print("Split size:", len(splits))
    for context in splits:
        response = generate_question_answer_own(context)
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
                dataset['context'].extend([context]*4)
         
        numbers = [len(dataset['question']), len(dataset['context']), len(dataset['answer'])]
        print(numbers)
        numbers.sort()
        smallest = numbers[0]
        # diff = abs(len(dataset['question']) - len(dataset['context']))
        # print(diff)
        # if diff != 0:
        dataset['context'] = dataset['context'][:smallest]
        dataset['question'] = dataset['question'][:smallest]
        dataset['answer'] = dataset['answer'][:smallest]
        print(len(dataset['context']), len(dataset['question']), len(dataset['answer']))   
    return dataset

if __name__ == '__main__':
    file_path = './pregnancy/21.txt'
    dataset = main(file_path)
    df = pd.DataFrame.from_dict(dataset)
    df.to_csv('./pregnancy/21.csv')