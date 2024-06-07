from flask import Flask, request, jsonify
import subprocess
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "Flask app is running"

@app.route('/link-website', methods=['POST'])
def link_website():
    website_url = request.json.get('websiteUrl')
    if not website_url:
        return jsonify({"error": "Invalid URL"}), 400

    current_dir = os.path.dirname(os.path.abspath(__file__))
    webcrawler_dir = os.path.join(current_dir, 'webcrawler')

    try:
        process = subprocess.Popen(
            ['scrapy', 'crawl', 'full_site_spider', '-a', f'start_url={website_url}'],
            cwd=webcrawler_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate(timeout=60)

        logging.info(f"Scrapy Output: {out.decode('utf-8')}")
        logging.error(f"Scrapy Error: {err.decode('utf-8')}")

        if process.returncode != 0:
            return jsonify({"error": "Scrapy command failed", "details": err.decode('utf-8')}), 500
    except subprocess.TimeoutExpired:
        process.kill()
        out, err = process.communicate()
        logging.error(f"Scrapy command timed out. Output: {out.decode('utf-8')}, Error: {err.decode('utf-8')}")
        return jsonify({"error": "Scrapy command timed out", "details": err.decode('utf-8')}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

    return jsonify({"message": "Website data is being processed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
