from flask import Flask, render_template, request
import sqlite3
import json

app = Flask(__name__)
DB_PATH = 'data.db'

def query_nodes(node_id=None, start=None, end=None, hops=None, mqtt=None):
    query = 'SELECT node_id, timestamp, hops, mqtt, raw_json FROM nodes WHERE 1=1'
    params = []
    if node_id:
        query += ' AND node_id = ?'
        params.append(node_id)
    if start:
        query += ' AND timestamp >= ?'
        params.append(start)
    if end:
        query += ' AND timestamp <= ?'
        params.append(end)
    if hops is not None:
        query += ' AND hops = ?'
        params.append(hops)
    if mqtt is not None:
        query += ' AND mqtt = ?'
        params.append(1 if mqtt else 0)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(query, params)
        rows = c.fetchall()
        return [
            {
                'node_id': r[0],
                'timestamp': r[1],
                'hops': r[2],
                'mqtt': bool(r[3]),
                'raw_json': json.loads(r[4]),
            }
            for r in rows
        ]

@app.route('/')
def index():
    node_id = request.args.get('node_id')
    start = request.args.get('start')
    end = request.args.get('end')
    hops = request.args.get('hops')
    hops = int(hops) if hops else None
    mqtt = request.args.get('mqtt')
    mqtt = mqtt.lower() == 'true' if mqtt else None
    data = query_nodes(node_id, start, end, hops, mqtt)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
