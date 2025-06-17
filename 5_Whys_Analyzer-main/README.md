# 5 Whys Analyzer

A simple Python tool for conducting 5 Whys root cause analysis with a web interface and a local LLM backend (Ollama).

## Features

- Web interface served with Flask using a standalone HTML file
- Uses a local LLM model via [Ollama](https://ollama.com/) (default: llama3, can be changed in code)
- Guides users through the 5 Whys root cause analysis process
- Outputs a formatted summary in your browser
- Works as long as the HTML and Python file are in the same directory

## Tech Stack

- Python 3.x
- Flask
- Requests
- Ollama (for running a local language model)

## Requirements

- [Ollama](https://ollama.com/download) installed and running on your machine
- The chosen LLM model pulled and available in Ollama (default: llama3)

## How to Run

1. **Install required Python packages (in your terminal):**
   pip install flask requests

2. **Download and run Ollama**
   - Download Ollama: https://ollama.com/download
   - Start Ollama (make sure it’s running)
   - Pull the required model (default is llama3):
     ollama pull llama3

3. **Project structure (must be like this):**
   5_Whys_Analyzer/
   
   - 5_Whys.py         # Main Python Flask app
   - index.html        # HTML interface (must be in the same folder as 5_Whys.py)
   - README.md

5. **Start the Flask server:**
   python 5_Whys.py

6. **Open your browser and go to:**
   http://localhost:5000  
   (or whatever address/port Flask tells you in the terminal)

7. **Use the web form to enter your problem statement and view the results.**

## Model Information

- The default model is `llama3`, but you can change the model name in the Python code by editing the `get_ollama_question` function.
- Ollama must be running locally for the app to work.

## Author

Mohit Gajula
