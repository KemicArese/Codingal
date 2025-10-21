import requests
import html

API_URL = "https://opentdb.com/api.php?amount=10&type=boolean"

def fetch_true_false_questions():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0 and data['results']:
            return data['results']
    return None

def run_true_false_questions():
    questions = fetch_true_false_questions()
    if not questions:
        print("Failed to retrieve questions. Please try again later.")
        return

    score = 0
    print("Welcome to the True/False Trivia Quiz!\n")
    for i, q in enumerate(questions):
        question = html.unescape(q['question'])
        correct_answer = html.unescape(q['correct_answer'])
        print(f"Question {i+1}: {question}")
        print("  1. True")
        print("  2. False")

        while True:
            try:
                choice = int(input("\nYour answer (1-2): "))
                if 1 <= choice <= 2:
                    break
                else:
                    print("Please enter a number between 1 and 2.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 2.")

        if (choice == 1 and correct_answer == "True") or (choice == 2 and correct_answer == "False"):
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {correct_answer}\n")

    print(f"Quiz Over! Your final score is {score} out of {len(questions)}.")
    print("Percentage Score: {:.2f}%".format((score / len(questions)) * 100))

if __name__ == "__main__":
    run_true_false_questions()