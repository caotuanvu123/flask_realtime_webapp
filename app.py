import redis
from flask import Flask, Response, request
from flask_cors import CORS
from connections.redis_conn import r

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:8989"])
# Redis connection

def event_stream(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")
            yield f"data: {message['data'].decode('utf-8')}\n\n"


@app.route('/stream/order_book')
def stream_order_book():
    symbol = request.args.get('symbol', 'btcusd_perp')
    channel = f'order_book_channel_{symbol}'

    return Response(event_stream(channel), content_type='text/event-stream')


@app.route('/stream/aggs_trade')
def stream_aggs_trade():
    symbol = request.args.get('symbol', 'btcusd_perp')
    channel = f'aggs_trade_channel_{symbol}'
    return Response(event_stream(channel), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
