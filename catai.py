import os
import re
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
            {"role": "user", "content": "Think of an object and name it."}
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


def generate_question(context):
    """
    Asks GPT-3 to generate the next question or make a guess based on the context of previous Q&A.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant. Your task is to guess an object by asking yes/no "
                                          "questions. Determine your next question or make a guess based on the "
                                          "conversation history."},
            {"role": "user", "content": context}
        ]
    )
    return response['choices'][0]['message']['content']


def is_question(input_text):
    """
    Determine if the input text is a question based on common question words and punctuation.
    """
    question_keywords = ['is', 'can', 'do', 'how', 'what', 'where', 'why', 'are', 'does', 'could', 'would', 'should']
    text = input_text.lower().strip()
    if text.endswith('?'):
        return True
    if any(text.startswith(word) for word in question_keywords):
        return True
    if re.search(r'\b(?:is|are|can|do|does|how|what|where|when|why|which)\b', text):
        return True
    return False


def play_game_guess_gpt():
    object_description = ask_gpt_to_think_of_object()
    tries_left = 5
    correct_guess = False

    print("GPT has 'thought' of an object. Try to guess it or ask yes/no questions about it!")

    while tries_left > 0 and not correct_guess:
        user_input = input("Your turn (ask a question or make a guess):\n").strip()

        if is_question(user_input):
            answer = ask_yes_no_question_about_object(object_description, user_input)
            print(f"GPT says: {answer}")
        else:
            confirmation = confirm_guess_with_gpt(object_description, user_input)
            if 'yes' in confirmation:
                print("Correct! You guessed the object GPT had in mind.")
                correct_guess = True
            else:
                tries_left -= 1
                print(f"No, that's not it. You have {tries_left} tries left.")

    if not correct_guess:
        print("Oh no! You've run out of tries! The game is over.")
        print(f"The object GPT had in mind was described as: {object_description}")

    # Ask if the user wants to play again
    play_again = input("Would you like to play again? [Y/N]").strip().lower()
    if play_again == 'y':
        play_game()

def play_game_guess_user():
    context = ""
    tries_left = 5
    correct_guess = False

    print("Think of an object, and I'll try to guess it by asking yes/no questions.")

    while tries_left > 0 and not correct_guess:
        next_move = generate_question(context).strip()

        if '?' in next_move:
            # It's a question
            print(next_move)
            user_answer = input("Your answer (yes/no): ").strip().lower()
            context += f"Q: {next_move} A: {user_answer}\n"  # Update context with the Q&A
        else:
            # It's a guess
            print(f"My guess: {next_move}. Am I right?")
            user_answer = input("Is my guess correct? (yes/no): ").strip().lower()
            if user_answer == 'yes':
                print("Great! I guessed it right!")
                correct_guess = True
            else:
                context += f"I guessed: {next_move}, but that was incorrect.\n"  # Update context with the incorrect guess
                tries_left -= 1
                print(f"No, that's not it. I have {tries_left} tries left.")

    if not correct_guess:
        print("I couldn't guess your object this time.")

    # Ask if the user wants to play again
    play_again = input("Would you like to play again? (yes/no): ").strip().lower()
    if play_again == 'yes':
        play_game()

def play_game():
    print("Welcome Cat Game!")
    print("Choose a mode to play:")
    print("1. Guess the object GPT is thinking of")
    print("2. Let GPT guess the object you're thinking of")
    mode = input("Enter 1 or 2: ").strip()

    if mode == '1':
        play_game_guess_gpt()
    elif mode == '2':
        play_game_guess_user()
    else:
        print("Invalid mode selected. Please try again.")
        play_game()

play_game()