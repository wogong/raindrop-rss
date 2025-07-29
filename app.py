from flask import Flask, Response, request
import json
import os
import logging
from dotenv import load_dotenv
from raindrop import RaindropClient

logging.basicConfig(level=logging.INFO)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
PERPAGE = os.environ.get('PERPAGE')

app = Flask(__name__)

@app.route('/')
def all_items_feed():
    """Generate RSS feed from all Raindrop.io items"""
    if ACCESS_TOKEN is None:
        return "Raindrop.io not configured", 404
    
    # Get query parameters with defaults
    perpage = request.args.get('perpage', default=PERPAGE, type=int)
    page = request.args.get('page', default=0, type=int)
    client = RaindropClient(access_token=ACCESS_TOKEN, perpage=perpage, page=page)
    
    try:
        feed = client.generate_feed(
            title="All Raindrop.io Items",
            description="All items from Raindrop.io"
        )
        return Response(feed, mimetype='application/xml')
    except Exception as e:
        logging.exception("Error generating Raindrop.io feed")
        return "An internal error has occurred.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
