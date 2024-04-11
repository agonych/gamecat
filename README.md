# Decision Tree Guessing Game

## Overview
This project implements a simple yet interactive game where a computer program tries to guess objects thought of by the user through a series of yes/no questions. Base version is utilizing a decision tree to learn from each interaction, expanding its knowledge base with every new object introduced by the user. AI version utilizes GPT API to offer two modes of play: AI trying to guess the object or AI thinking of an object for the user to guess.

## Features
- **Iterative Learning**: With each play through, the game's decision tree grows, becoming smarter and more capable of guessing a wider range of objects.
- **User Input Variation Handling**: Accepts variations of yes (y, yes, yep) and no (n, no, nope, none) answers to improve user experience.
- **Simple Text Interface**: Easy-to-navigate textual interface for straightforward play and learning.

## How to Play
1. Think of an object.
2. The game will begin by asking a series of yes/no questions to narrow down what the object might be.
3. If the game guesses wrong, it will ask you what the object was and request a distinguishing question to differentiate this new object from others.
4. The game learns this new information for future guesses.

## Installation
This game is written in Python and can be run with any Python interpreter without the need for additional libraries.

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/agonych/gamecat
```

To run the base version, navigate to the project directory and run the game with:

```bash
python cat.py
```

To run the AI version, you will need to set up an OpenAI API key and install the OpenAI Python library. Once you have your API key, create a `.env` file in the project directory with the following content:

```bash
GPT_API_KEY=[your_api_key_here]
```

Then, install the necessary libraries

```bash
pip install -r requirements.txt
```

You can now run the AI version of the game with:

```bash
python catai.py
```

## Contribution
Feel free to fork this project, make improvements, or suggest changes by creating a pull request. We welcome contributions that enhance the game, such as new features, bug fixes, or improved documentation.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.
```

[]: # Path: LICENSE
Apache License

Version 2.0, January 2004

http://www.apache.org/licenses/


