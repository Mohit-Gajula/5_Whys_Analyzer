import os
from flask import Flask, request, render_template_string, session
import requests
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

script_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(script_dir, "index.html")
with open(html_path, "r", encoding="utf-8") as file:
    HTML = file.read()


def get_ollama_question(prompt, model='llama3'):
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(api_url, json=payload)
        resp.raise_for_status()
        response_json = resp.json()
        if "response" in response_json:
            return response_json["response"].strip()
        else:
            return "Error: No valid response from LLM."
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"

def format_summary(summary):
    # Make bold headings stand out and add line breaks after them
    summary = re.sub(r'\*\*Root Cause:\*\*', r'<b>Root Cause:</b><br>', summary)
    summary = re.sub(r'\*\*Recommendation for Next Steps:\*\*', r'<br><b>Recommendation for Next Steps:</b><br>', summary)
    # Turn **1.**, **2.** etc into an HTML unordered list
    if "**1.**" in summary:
        # Find all numbered points and wrap in <ul><li>
        points = re.split(r'\*\*(\d+)\.\*\*', summary)
        new_summary = points[0]
        if len(points) > 1:
            new_summary += "<ul>"
            for i in range(1, len(points)-1, 2):
                new_summary += f"<li><b>{points[i]}.</b> {points[i+1].strip()}</li>"
            new_summary += "</ul>"
        summary = new_summary
    # Convert remaining line breaks
    summary = summary.replace('\n', '<br>')
    return summary

@app.route("/", methods=["GET", "POST"])
def index():
    if "qas" not in session:
        session["qas"] = []
    if request.method == "POST":
        if "problem" not in session:
            session["problem"] = request.form["problem"].strip()
        else:
            user_answer = request.form["answer"].strip()
            qas = session["qas"]
            qas.append((session["current_question"], user_answer))
            session["qas"] = qas

        problem = session["problem"]
        qas = session["qas"]
        prompt = (
            "You are a root cause analysis expert. "
            "For each round, you will be given the problem and all previous answers. "
            "Do not just ask 'why?'—ask a specific, probing question that logically follows from the last answer. "
            "Keep each question concise and context-aware.\n\n"
            f"Problem: {problem}\n"
        )
        for i, (q, a) in enumerate(qas, 1):
            prompt += f"Q{i}: {q}\nA{i}: {a}\n"
        if len(qas) < 5:
            if len(qas) == 0:
                prompt += "Ask your first question:"
            else:
                prompt += "Ask your next question:"
            question = get_ollama_question(prompt)
            session["current_question"] = question
            return render_template_string(
                HTML,
                question=question,
                qas=qas,
                problem=problem,
                show_summary=False
            )
        else:
            # All 5 whys done, get summary
            summary_prompt = (
                "Based on the following 5 Whys analysis (problem, questions, and answers), "
                "provide a brief summary of the root cause and a recommendation for next steps.\n"
                f"Problem: {problem}\n"
            )
            for i, (q, a) in enumerate(qas, 1):
                summary_prompt += f"Q{i}: {q}\nA{i}: {a}\n"
            raw_summary = get_ollama_question(summary_prompt)
            summary = format_summary(raw_summary)
            # Clear session for next run
            session.pop("problem", None)
            session.pop("qas", None)
            session.pop("current_question", None)
            return render_template_string(
                HTML,
                summary=summary,
                qas=qas,
                problem=problem,
                show_summary=True
            )

    # Initial GET request
    return render_template_string(HTML, show_summary=False, problem=None, qas=None)

if __name__ == "__main__":
    app.run(debug=True)
