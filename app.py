from flask import Flask, request, jsonify, render_template_string
import tempfile
import os
from docx import Document
import re

app = Flask(__name__)

# simple MathML placeholder converter -> LaTeX (improve later)
def mathml_to_latex(text):
    # Placeholder heuristics: if text contains <m:oMath> or OMath markers, wrap as latex tag
    if '<m:oMath' in text or 'OMath' in text:
        # This is a naive substitution; replace with actual MathML->LaTeX if available
        return re.sub(r'<[^>]+>', '', text).strip() or '<latex_equation>'
    return text

# Parse docx tables into the JSON structure
def parse_docx_tables(path):
    doc = Document(path)
    results = []

    for table in doc.tables:
        q = {
            'question': '',
            'type': '',
            'options': [],
            'solution': '',
            'marks': {'correct': 0, 'incorrect': 0}
        }

        for row in table.rows:
            cells = [c.text.strip() for c in row.cells]
            if not cells or not cells[0]:
                continue

            key = cells[0].strip().lower()

            if key == 'question':
                q_text = ' '.join(c for c in cells[1:] if c)
                q['question'] = mathml_to_latex(q_text)
            elif key == 'type':
                q['type'] = cells[1] if len(cells) > 1 else ''
            elif key == 'option':
                text = cells[1] if len(cells) > 1 else ''
                status = cells[2] if len(cells) > 2 else ''
                q['options'].append({'text': mathml_to_latex(text), 'status': status})
            elif key == 'solution':
                sol_text = ' '.join(c for c in cells[1:] if c)
                q['solution'] = mathml_to_latex(sol_text)
            elif key == 'marks':
                correct = int(cells[1]) if len(cells) > 1 and cells[1].isdigit() else 0
                incorrect = int(cells[2]) if len(cells) > 2 and cells[2].isdigit() else 0
                q['marks'] = {'correct': correct, 'incorrect': incorrect}

        results.append(q)

    return results

@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
    <!doctype html>
    <title>Upload DOCX</title>
    <h1>Upload DOCX to convert to JSON</h1>
    <form method=post enctype=multipart/form-data action='/upload'>
      <input type=file name=file accept='.docx' />
      <input type=submit value=Upload />
    </form>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'no selected file'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        f.save(tmp.name)
        try:
            data = parse_docx_tables(tmp.name)
        finally:
            os.unlink(tmp.name)

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
