# app.py
from flask import Flask, render_template, request, redirect, url_for, abort
import re
from database import init_db, save_url, get_original_url

app = Flask(__name__)

# Initialize database on startup
init_db()

def is_valid_url(url):
    # Basic URL validation regex
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and pattern.match(url)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('url', '').strip()
        if not long_url:
            return render_template('error.html', message="URL cannot be empty.")
        if not is_valid_url(long_url):
            return render_template('error.html', message="Please enter a valid URL (must start with http:// or https://).")
        
        short_code = save_url(long_url)
        short_url = request.url_root + short_code  # e.g., http://localhost:5000/abc123
        return render_template('index.html', short_url=short_url, long_url=long_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    original_url = get_original_url(short_code)
    if original_url:
        return redirect(original_url, code=302)
    else:
        abort(404)

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', message="Short link not found."), 404

if __name__ == '__main__':
    app.run(debug=True)