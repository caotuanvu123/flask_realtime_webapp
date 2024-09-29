import redis
from flask import Flask, Response, request
from flask_cors import CORS
from connections.redis_conn import r

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])
# Redis connection

def event_stream(symbol):
    pubsub = r.pubsub()
    channel = f'order_book_channel_{symbol}'  # Subscribe to a symbol-specific channel
    pubsub.subscribe(channel)

    # Stream the messages to the client
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")
            yield f"data: {message['data'].decode('utf-8')}\n\n"

# Stream Order Book for a specific symbol
@app.route('/stream/order_book')
def stream_order_book():
    symbol = request.args.get('symbol', 'btcusd_perp')
    return Response(event_stream(symbol), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
