import os
import pickle

"""
A decision-tree based learning game that iteratively guesses objects by asking yes/no questions, adapting to new knowledge from user input
"""

class TreeNode:
    """
    A node in the decision tree
    @param question: The question to ask at this node
    @param yes: The child node if the answer is yes
    @param no: The child node if the answer is no
    """
    # Initialize the node with a question and two child nodes
    def __init__(self, question=None, yes=None, no=None):
        # The question to ask at this node
        self.question = question
        # The child node if the answer is yes
        self.yes = yes
        # The child node if the answer is no
        self.no = no


"""
Inserts a new node with a question and object as children of the parent node
@param parent_node: The parent node to insert the new node under
@param question: The question to ask at the new node
@param new_object: The object to guess at the new node
@return: The parent node with the new node inserted
"""
def insert_node(parent_node, question, new_object, is_yes):
    # Creating a new node for the new object
    new_object_node = TreeNode(new_object)
    # Placing the new question and new object in the tree
    if is_yes:
        # if the answer is yes, insert the new question and object as children of the parent node for the yes branch
        parent_node.yes = TreeNode(question, new_object_node, parent_node.no)
    else:
        # if the answer is no, insert the new question and object as children of the parent node for the no branch
        parent_node.no = TreeNode(question, new_object_node, parent_node.yes)


"""
Prompts the user for the correct object and the difference between the correct object and the current object
@param node_question: The question at the current node
@return: The correct object and the new question based on the difference
"""
def learn_new_object(node_question):
    # Prompt the user for the correct object and the difference
    new_object = input("I give up. What is it? ").strip().lower()
    # Collect the difference between the correct object and the current object
    difference = input(f"How does {new_object} differ from {node_question}? ").strip().lower() # Save in lowercase
    # Create a new question based on the difference
    new_question = f"Is it {difference}?"
    # Return the correct object and the new question
    return new_object, new_question


"""
Asks a question at the current node and recursively navigates the tree based on the user's input
@param node: The current node in the decision tree
@param parent: The parent node of the current node (default is None)

@return: The updated root node of the decision tree
"""
def ask_question(node, parent=None):
    # Check if the node is a question node
    if node.question.endswith('?'):
        # Ask the question and get the user's input
        answer = input(node.question + " (yes/no): ").strip().lower()
        # Check only the first letter for simplicity
        if answer.startswith('y'):
            # If the answer is yes, navigate to the yes branch
            if node.yes is None:
                # If the yes branch is None, the object has been guessed correctly
                print("I guessed right!")
                return None
            else:
                # Recursively navigate to the yes branch
                return ask_question(node.yes, node)
        # If the answer is no, navigate to the no branch
        elif answer.startswith('n'):
            # If the no branch is None, the object has not been guessed correctly
            if node.no is None:
                # Learn the correct object and the difference
                new_object, new_question = learn_new_object(node.question[:-1])
                # Insert the new node with the new question and object
                insert_node(node, new_question, new_object, False)
                # return the updated node
                return node
            else:
                # Recursively navigate to the no branch
                return ask_question(node.no, node)
    else:
        # If the node is not a question node, prompt the user for the correct object
        answer = input(f"Is it {node.question}? (yes/no): ").strip().lower()  # Handle input in lowercase
        # Check only the first letter for simplicity
        if answer.startswith('y'): # If the answer is yes, the object has been guessed correctly
            print("I guessed right!")
        elif answer.startswith('n'): # If the answer is no, prompt the user for the correct object and the difference
            # Learn the correct object and the difference
            new_object, new_question = learn_new_object(node.question)
            # Insert the new node with the new question and object
            new_node = TreeNode(new_question, TreeNode(new_object), TreeNode(node.question))
            # Check if the current node has a parent
            if parent:
                # Check if the current node is the yes branch or the no branch of the parent node
                if parent.yes == node:
                    # Update the yes branch of the parent node with the new node
                    parent.yes = new_node
                else:
                    # Update the no branch of the parent node with the new node
                    parent.no = new_node
            else:
                # Return the new node
                return new_node
        return None


"""
Save the decision tree to a file within the data directory.
@param root_node: The root node of the decision tree
@param directory: The directory to save the tree to (default is 'data')
@param filename: The name of the file to save the tree to (default is 'tree.pkl')
@return: None
"""
def save_tree(root_node, directory="data", filename='tree.pkl'):
    # Check if the directory exists, create it if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Construct the file path to save the tree
    filepath = os.path.join(directory, filename)
    # Save the tree to the file
    with open(filepath, 'wb') as file:
        pickle.dump(root_node, file)


"""
Load the decision tree from a file or create a new one if the file doesn't exist or an error occurs.
@param directory: The directory to load the tree from (default is 'data')
@param filename: The name of the file to load the tree from (default is 'tree.pkl')
@return: The loaded tree or a new tree with "cat" as the root node
"""
def load_tree(directory="data", filename='tree.pkl'):
    # Construct the file path to load the tree
    filepath = os.path.join(directory, filename)
    try:
        # Load the tree from the file
        with open(filepath, 'rb') as file:
            # Return the loaded tree
            return pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        # If the file doesn't exist, or an error occurs, return a new tree with "cat" as the root node.
        return TreeNode("cat")


# Starting node of the tree
root = load_tree()

"""
Plays the game by asking questions and navigating the decision tree based on user input (infinitely until the user decides to stop)
@param root: The root node of the decision tree
"""
def play_game(root):
    # Print the initial message
    print("Think of something...")
    # Start the game by asking questions and navigating the tree
    new_root = ask_question(root)
    # Return the updated root node
    return new_root if new_root else root

# Play the game
while True:
    # Play the game with the current root node
    root = play_game(root)
    # Save the tree after each game
    save_tree(root)
    # Ask the user if they want to play again
    if not input("Do you want to play again? (yes/no): ").strip().lower().startswith('y'):
        # If the user does not want to play again, break the loop
        break
