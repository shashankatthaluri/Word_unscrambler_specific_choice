import requests  # Import the requests library for making HTTP requests
from flask import Flask, render_template, request  # Import necessary modules from Flask

app = Flask(__name__)  # Create a Flask application instance

# Function to download words from a URL
def download_words():
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"  # Define the URL of the word list
    response = requests.get(url)  # Send an HTTP GET request to the URL
    if response.status_code == 200:  # If the request is successful
        return response.text.splitlines()  # Return the text content of the response split into lines (words)
    else:  # If the request fails
        raise Exception("Failed to download word list")  # Raise an exception indicating failure

# Sample word list (replace with your own word list)
word_list = download_words()  # Call the download_words() function to get the word list

# Function to filter words based on user criteria
def filter_words(words, length=None, must_include=None, avoid=None, must_include_positions=None, avoid_positions=None):
    filtered_words = []  # Initialize an empty list to store filtered words
    for word in words:  # Iterate over each word in the word list
        if length and len(word) != length:  # If length is specified and the word length doesn't match
            continue  # Skip to the next word
        if must_include and not all(char in word for char in must_include):  # If must_include letters are specified and any of them are not in the word
            continue  # Skip to the next word
        if avoid and any(char in word for char in avoid):  # If avoid letters are specified and any of them are in the word
            continue  # Skip to the next word
        if must_include_positions and not all(word[pos - 1] == char for char, pos in must_include_positions):  # If specific positions to include are specified and they don't match
            continue  # Skip to the next word
        if avoid_positions and any(word[pos - 1] == char for char, pos in avoid_positions):  # If specific positions to avoid are specified and any of them match
            continue  # Skip to the next word
        filtered_words.append(word)  # If all criteria are met, add the word to the filtered list
    return filtered_words  # Return the filtered list of words

# Home route
@app.route('/', methods=['GET', 'POST'])  # Define a route for the home page that handles both GET and POST requests
def home():
    if request.method == 'POST':  # If a POST request is received (form submitted)
        length = request.form['length']  # Get the value of the 'length' field from the form
        must_include = request.form['must_include'].lower()  # Get the value of the 'must_include' field from the form and convert to lowercase
        avoid = request.form['avoid'].lower()  # Get the value of the 'avoid' field from the form and convert to lowercase
        must_pos = request.form['must_pos']  # Get the value of the 'must_pos' field from the form
        avoid_pos = request.form['avoid_pos']  # Get the value of the 'avoid_pos' field from the form
        
        # Check if at least one input is provided
        if not length and not must_include and not avoid and not must_pos and not avoid_pos:
            return "No input, please fill at least one box for the list"  # Return an error message
        
        length = int(length) if length.isdigit() else None  # Convert length to an integer if it consists of digits
        must_include = must_include.split() if must_include else None  # Split must_include string into a list of characters if it's not empty
        avoid = avoid.split() if avoid else None  # Split avoid string into a list of characters if it's not empty
        must_include_positions = [(pos[0], int(pos[1:])) for pos in must_pos.split() if pos] if must_pos else None  # Split must_pos string into a list of tuples (char, position) if it's not empty
        avoid_positions = [(pos[0], int(pos[1:])) for pos in avoid_pos.split() if pos] if avoid_pos else None  # Split avoid_pos string into a list of tuples (char, position) if it's not empty
        
        # Filter words based on user criteria
        filtered_words = filter_words(word_list, length, must_include, avoid, must_include_positions, avoid_positions)
        
        # Check if no words are found
        if not filtered_words:
            return "Sorry, no words found in our database 😢, please fill your requirements carefully and try again"  # Return a message indicating no words found
        
        return render_template('index.html', filtered_words=filtered_words)  # Render the index.html template with filtered words
    
    return render_template('index.html')  # Render the index.html template for GET requests

if __name__ == '__main__':
    app.run(debug=True, port=5143)  # Run the Flask application
