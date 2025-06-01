from flask import Flask, render_template_string, send_file, request, redirect
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os

# Create Flask app
app = Flask(__name__)

# Load data helper function
def load_data():
    try:
        return pd.read_csv("data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Age", "Score"])

@app.route('/')
def home():
    df = load_data()
    if df.empty:
        return "<h1>No data found in data.csv</h1>"

    top = df.loc[df['Score'].idxmax()]
    avg = df['Score'].mean()

    html = f"""
    <h1>📊 Python Data Dashboard</h1>

    <form action="/upload" method="POST" enctype="multipart/form-data">
        <label>Upload CSV:</label>
        <input type="file" name="csv_file" required>
        <button type="submit">Upload</button>
    </form>
    <hr>

    <h2>Summary:</h2>
    {df.describe().to_html()}
    <h3>🏆 Top Scorer: {top['Name']} with {top['Score']} points</h3>
    <h3>📈 Average Score: {avg:.2f}</h3>
    <a href="/graph">🔍 View Score Graph</a> | 
    <a href="/download-graph">⬇️ Download Score Graph</a>
    """
    return render_template_string(html)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['csv_file']
    if file:
        file.save('data.csv')  # Overwrite existing CSV
    return redirect('/')

@app.route('/graph')
def show_graph():
    df = load_data()
    if df.empty:
        return "<h2>No data available to plot.</h2>"

    fig, ax = plt.subplots()
    ax.bar(df['Name'], df['Score'], color='orange')
    ax.set_title('Scores by Name')
    ax.set_xlabel('Name')
    ax.set_ylabel('Score')

    # Save for download
    fig.tight_layout()
    fig.savefig('static/score_chart.png')

    # Also return for browser display
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

@app.route('/download-graph')
def download_graph():
    return send_file('static/score_chart.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    