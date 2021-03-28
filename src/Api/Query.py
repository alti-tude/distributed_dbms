from . import app

@app.route("/query", methods=["GET", "POST"])
def Query()