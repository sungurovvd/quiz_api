import json
import os
import requests
from flask import Flask, request
from datetime import datetime
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


def create_question_table():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS questions (
        id SERIAL PRIMARY KEY,
        question_text TEXT,
        answer_text TEXT,
        created_at TIMESTAMP
    )
    '''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()


def get_random_question():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    select_query = '''
    SELECT * FROM questions ORDER BY RANDOM() LIMIT 1
    '''
    cursor.execute(select_query)
    question = cursor.fetchone()
    cursor.close()
    connection.close()

    if question:
        question_data = {
            'id': question[0],
            'question_text': question[1],
            'answer_text': question[2],
            'created_at': question[3].isoformat()
        }
    else:
        question_data = {}

    return json.dumps(question_data)


def get_last_question():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    select_query = '''
    SELECT * FROM questions ORDER BY id DESC LIMIT 1
    '''
    cursor.execute(select_query)
    question = cursor.fetchone()
    cursor.close()
    connection.close()

    if question:
        question_data = {
            'id': question[0],
            'question_text': question[1],
            'answer_text': question[2],
            'created_at': question[3].isoformat()
        }
    else:
        question_data = {}

    return json.dumps(question_data)


def find_question(question):
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    select_query = f"SELECT EXISTS (SELECT 1 FROM questions WHERE question_text=%s);"
    cursor.execute(select_query, (question, ))
    answer = cursor.fetchone()
    cursor.close()
    connection.close()
    print(f'answer exist:{answer[0]}')

    return answer[0]


def save_question(question_text, answer_text):
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    insert_query = '''
    INSERT INTO questions (question_text, answer_text, created_at)
    VALUES (%s, %s, %s)
    '''
    current_time = datetime.now()
    cursor.execute(insert_query, (question_text, answer_text, current_time))
    connection.commit()
    cursor.close()
    connection.close()


def fetch_question_from_api(questions_num):
    while True:
        url = f"https://jservice.io/api/random?count={questions_num}"
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            break
    print(f'response:{response}')
    json_data = response.json()
    return json_data


@app.route('/questions', methods=['POST', 'GET'])
def generate_questions():
    if request.method == 'POST':

        if request.is_json:
            data = request.get_json()
            question = get_last_question()

            for _ in range(data['questions_num']):
                unique_question = False
                while not unique_question:
                    question_data = fetch_question_from_api(1)
                    question_text = question_data[0]['question']
                    answer_text = question_data[0]['answer']

                    if find_question(question_text) is False:
                        unique_question = True

                save_question(question_text, answer_text)

            return question, 201
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        question = get_random_question()
        return question


if __name__ == '__main__':
    create_question_table()
    app.run(host='0.0.0.0', port=5000)
