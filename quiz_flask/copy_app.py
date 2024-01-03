from flask import Flask, render_template, request, redirect, url_for
import requests
import random
import time

app = Flask(__name__)

def get_countries_and_capitals():
    url = "https://restcountries.com/v2/all"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        countries_and_capitals = {country['name']: country.get('capital', 'N/A') for country in data}
        return countries_and_capitals
    else:
        return {}

questions = get_countries_and_capitals()
previous_questions = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

def generate_que():
    while True:
        que = random.choice(list(questions.items()))
        if que not in previous_questions and que[1] != 'N/A':
            previous_questions.append(que)
            return que
    
def validate_answer(correct_answer, user_answer):
    return user_answer == correct_answer

@app.route('/over/<int:score>')
def over(score):
    return render_template('over.html', score=score)

@app.route('/submit_answer',  methods=['POST'])
def submit_answer():
    #retrieving the values
    score = request.form.get('current_score')
    score = int(score) if score.isdigit() else 0
    correct_answer = request.form.get('correct_answer')
    user_answer = request.form.get('user_answer')
    
    #validating the answer
    if validate_answer(correct_answer, user_answer):
        new_score = score + 1
        return redirect(url_for('quiz', score = new_score))
    else:
        return redirect(url_for('over', score = score))

@app.route('/quiz')
def quiz():
    score = request.args.get('score', '0')
    selected_answers = []
    new_que = generate_que()
    correct_ans = new_que[1]
    selected_answers.append(correct_ans)
    selected_answers.append(generate_que()[1])
    selected_answers.append(generate_que()[1])
    selected_answers.append(generate_que()[1])
    random.shuffle(selected_answers)
    print("New que is", new_que)
    return render_template('quiz.html',correct_answer=correct_ans, selected_answers=selected_answers, question=new_que, score=score)

if __name__ == '__main__':
    app.run(debug=True)
