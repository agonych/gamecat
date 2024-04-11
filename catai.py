import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv('GPT_API_KEY')
)


def ask_gpt_to_think_of_object():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Think of an object and describe it."}
        ]
    )
    object_description = response['choices'][0]['message']['content']
    return object_description


def ask_yes_no_question_about_object(object_description, question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant who knows about the object: {object_description}."},
            {"role": "user", "content": question}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer.strip().lower()


def confirm_guess_with_gpt(object_description, guess):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant who knows the object: {object_description}."},
            {"role": "user", "content": f"Is the object a {guess}?"}
        ]
    )
    confirmation = response['choices'][0]['message']['content']
    return confirmation.strip().lower()


def play_game():
    object_description = ask_gpt_to_think_of_object()
    tries_left = 5
    correct_guess = False

    print("I thought of an object. Try to guess it!")

    while tries_left > 0 and not correct_guess:
        user_input = input("Enter '1' to ask a yes/no question or '2' to guess the object.\n").strip()

        if user_input == '2':
            guess = input("What is your guess? ").strip().lower()
            confirmation = confirm_guess_with_gpt(object_description, guess)
            if 'yes' in confirmation:
                print("Correct! You guessed the object I have in mind.")
                correct_guess = True
            else:
                tries_left -= 1
                print(f"No, that's not it. You have {tries_left} tries left!")
        elif user_input == '1':
            question = input("Ask your yes/no question about the object.\n").strip()
            answer = ask_yes_no_question_about_object(object_description, question)
            print(f"GPT says: {answer}")
        else:
            print("Invalid input. Please enter '1' to ask a question or '2' to make a guess.")

    if not correct_guess:
        print("Oh no! You've run out of tries! The game is over.")
        print(f"The object I had in mind was: {object_description}")

    # Ask if the user wants to play again
    play_again = input("Would you like to play again? [Y/N]").strip().lower()
    if play_again.startswith('y'):
        play_game()


play_game()
