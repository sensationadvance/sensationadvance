import requests
import json
import sys
import os

def extract_text_from_json(file_paths: list[str]):
    combined_text = []
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            if not item["signature"]:
                combined_text.append(item["content"])
        
        # for item in data:
        #     if item["signature"]:
        #         combined_text.append(f"{item['content']} [ПЕЧАТЬ]")
    
    return " ".join(combined_text)

def askOllama(prompt, model, context):

    base_url = 'http://localhost:11434'
    endpoint = '/api/generate'

    prompt = prompt.strip()

    payload = {
        "model": model, 
        "stream": False,                            
        "prompt": prompt,
        "context": context   
    }
    response = requests.post(base_url + endpoint, json=payload)
    if response.status_code == 200:
        answer = response.json()

        text = answer.get("response")
        context = answer.get("context")

        response = {"text": text, "context": context}

        return response
    else:
        print(f"ollama error: {response}; {response.content}")
        exit(1)
        return None

def process_files(file_paths):
    print(file_paths)
    input_data = extract_text_from_json(file_paths)
    print(input_data)

    prompt = f"""
    Определи тип документа: сразу краткий ответ - "Паспорт" или "Трудовая"
    В трудовой профессии человека.
    В паспорте основные данные человека.
    Входные текстовые данные:
    {input_data}
    """    

    print("\n\n")
    print(askOllama(prompt, model, [])["text"])    
    print("\n---\n")

#трудовая_книжка = "08 09 10 07 01 07 05 03 03 2008 2008 2007 07 Запись за № как внесенная Принят специалиста на программного Уволен желанию по пункт 3 Трудового кодекса Генеральный недействительна ошибочно должность внедрению обеспечения по 1С собственному статьи 77 Российской Федерации директор Терехов Ф.С от Приказ 01.05.2007 № 4 от Приказ 07.03.2008 № 1 ."
#трудовая_книжка_2 = "27 01 04 2005 ООО Фирма Свилон Принят на должность Приказ №9 от 31.03.2005 28 30 04 2005 29 машиниста эскаватора по Уволен собственному Приказ №25 желанию согласно пункта 3 от 30.04.2005 Кодекса Трудового 77 статьи Российской Федерации Генеральный директор Туляков Ю. П."
#паспорт = "3 отделением милиции УВД Администрации Ногинского района Московской области 10.10.2002 502-067 .. Копаев Алексей Дмитриевич муж. гор. Челябинск 05.11.1981"
#предположительно_паспорт = "6 7 п.Зеленолугский июля 17 Молодежная кв.2"

if len(sys.argv) < 2:
    print("json file paths are required as argument!")
    exit(1)

path = sys.argv[1]

model = "mistral-nemo:12b"

input_paths = sys.argv[1:]

process_files(input_paths)

