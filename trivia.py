import requests
import random
import html

EDUCATION_CATEGORY_ID = 9
API_URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def fetch_education_questions():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0 and data['results']:
            return data['results']
    return None

def run_quiz():
    questions = fetch_education_questions()
    if not questions:
        print("Failed to retrieve questions. Please try again later.")
        return
    
    score = 0
    print("Welcome to the Education Trivia Quiz!\n")
    for i, q in enumerate(questions):
        questions = html.unescape(q['question'])
        correct_answer = html.unescape(q['correct_answer'])
        incorrect_answers = [html.unescape(ans) for ans in q['incorrect_answers']]
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)
        print(f"Question {i+1}: {questions}")
        for idx, option in enumerate(options):
            print(f"  {idx}. {option}")

        while True:
            try:
                choice = int(input("\nYour answer (1-4): "))
                if 1 <= choice <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
                if options[choice - 1] == correct_answer:
                    print("Correct!\n")
                    score += 1
                else:
                    print(f"Wrong! The correct answer was: {correct_answer}\n")
    print(f"Quiz Over! Your final score is {score} out of {len(questions)}.")
    print("Percentage Score: {:.2f}%".format((score / len(questions)) * 100))

if __name__ == "__main__":
    run_quiz()