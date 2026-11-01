from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>Student Result</title>
<h1>Student Result Application</h1>
<form method="post">
  <label>Student name <input name="name" required></label><br>
  <label>Subject 1 <input name="mark1" type="number" min="0" max="100" required></label><br>
  <label>Subject 2 <input name="mark2" type="number" min="0" max="100" required></label><br>
  <label>Subject 3 <input name="mark3" type="number" min="0" max="100" required></label><br>
  <button type="submit">Calculate result</button>
</form>
{% if error %}<p role="alert">{{ error }}</p>{% endif %}
{% if result %}
  <h2>Result for {{ result.name }}</h2>
  <p>Total: {{ result.total }}</p>
  <p>Average: {{ result.average }}</p>
  <p>Status: {{ result.status }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            marks = [int(request.form[f"mark{i}"]) for i in range(1, 4)]
            if not name or any(mark < 0 or mark > 100 for mark in marks):
                raise ValueError
            total = sum(marks)
            result = {
                "name": name,
                "total": total,
                "average": f"{total / 3:.2f}",
                "status": "PASS" if all(mark >= 35 for mark in marks) else "FAIL",
            }
        except (KeyError, ValueError):
            error = "Enter a name and three whole-number marks from 0 to 100."

    return render_template_string(PAGE, result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)