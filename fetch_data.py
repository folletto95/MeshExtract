import requests
import sqlite3
import json
import os

def fetch_nodes():
    url = os.environ.get('MESHSENSE_API_URL', 'https://api.meshsense.example/nodes')
    token = os.environ.get('MESHSENSE_API_TOKEN')
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def save_nodes(nodes, db_path='data.db'):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS nodes (id INTEGER PRIMARY KEY AUTOINCREMENT, node_id TEXT, timestamp TEXT, hops INTEGER, mqtt INTEGER, raw_json TEXT)'
        )
        for n in nodes:
            node_id = n.get('node_id')
            timestamp = n.get('timestamp')
            hops = n.get('hops')
            mqtt = 1 if n.get('mqtt') else 0
            raw_json = json.dumps(n)
            c.execute(
                'INSERT INTO nodes (node_id, timestamp, hops, mqtt, raw_json) VALUES (?,?,?,?,?)',
                (node_id, timestamp, hops, mqtt, raw_json),
            )
        conn.commit()

if __name__ == '__main__':
    data = fetch_nodes()
    save_nodes(data)
    print(f"Stored {len(data)} records")
