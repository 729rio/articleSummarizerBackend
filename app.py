from flask import Flask, request, jsonify
from summarization import summarize_article

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    summary = summarize_article(url)
    
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
