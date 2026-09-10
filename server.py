import argparse
import csv
import json
import math
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
FEATURES = ('temperature', 'humidity', 'moisture', 'ph', 'nitrogen', 'phosphorus', 'potassium')
CSV_COLUMNS = ('Temperature', 'Humidity', 'Soil Moisture', 'pH', 'N', 'P', 'K')
RANGES = dict(zip(FEATURES, (40, 100, 1000, 14, 200, 200, 200)))
DATASET_PATH = ROOT / 'recomendation.csv'
MAX_BODY_BYTES = 4096


def load_profiles():
    with DATASET_PATH.open(newline='', encoding='utf-8-sig') as file:
        rows = csv.DictReader(file)
        missing_columns = set(CSV_COLUMNS + ('Crop',)) - set(rows.fieldnames or ())
        if missing_columns:
            raise RuntimeError(f'{DATASET_PATH.name} is missing columns: {sorted(missing_columns)}')
        profiles = []
        for row in rows:
            if not row.get('Crop'):
                continue
            profiles.append({
                'crop': row['Crop'].strip(),
                'values': {
                    feature: float(row[column])
                    for feature, column in zip(FEATURES, CSV_COLUMNS)
                },
            })
    if not profiles:
        raise RuntimeError(f'{DATASET_PATH.name} does not contain any profiles')
    return profiles


PROFILES = load_profiles()


def predict(values):
    ranked = []
    for profile in PROFILES:
        distance = math.sqrt(sum(((values[key] - profile['values'][key]) / RANGES[key]) ** 2 for key in FEATURES))
        ranked.append({'crop': profile['crop'], 'distance': distance})
    ranked.sort(key=lambda item: item['distance'])
    winner = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else {'distance': winner['distance'] + 1}
    confidence = max(51, min(99, round((1 - winner['distance'] / (winner['distance'] + runner_up['distance'] + 0.001)) * 100)))
    return {'crop': winner['crop'], 'confidence': confidence}


def parse_values(payload):
    if not isinstance(payload, dict):
        raise ValueError('Request body must be a JSON object')
    values = {}
    for key in FEATURES:
        value = payload.get(key)
        if isinstance(value, bool) or value is None:
            raise ValueError('Send numeric values for all seven model features')
        try:
            number = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError('Send numeric values for all seven model features') from error
        if not math.isfinite(number) or number < 0 or number > RANGES[key]:
            raise ValueError(f'{key} must be between 0 and {RANGES[key]}')
        values[key] = number
    return values


class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/api/health':
            self.send_json(200, {
                'status': 'ok',
                'profiles': len(PROFILES),
                'crops': sorted({profile['crop'] for profile in PROFILES}),
            })
            return
        if path == '/api/profiles':
            self.send_json(200, {
                'profiles': sorted({profile['crop'] for profile in PROFILES}),
                'count': len(PROFILES),
            })
            return
        if path in ('/', '/code.html'):
            body = (ROOT / 'code.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_json(404, {'error': 'Not found'})

    def do_POST(self):
        if urlsplit(self.path).path != '/api/predict':
            self.send_json(404, {'error': 'Not found'})
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError('Request body is empty or too large')
            payload = json.loads(self.rfile.read(length))
            self.send_json(200, predict(parse_values(payload)))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {'error': 'Send numeric values from 0 to their allowed maximum for all seven model features'})
            return

    def do_HEAD(self):
        if urlsplit(self.path).path in ('/', '/code.html'):
            self.send_response(200)
            self.end_headers()
            return
        self.send_response(404)
        self.end_headers()

    def do_PUT(self):
        self.send_json(405, {'error': 'Method not allowed'})

    do_DELETE = do_PUT

    def log_message(self, format, *args):
        print(f'{self.address_string()} - {format % args}')


def get_lan_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(('8.8.8.8', 80))
            return sock.getsockname()[0]
    except OSError:
        return 'your-computer-ip'


def main():
    parser = argparse.ArgumentParser(description='Run the Fieldwise crop recommendation web app.')
    parser.add_argument('--host', default=os.getenv('HOST', '0.0.0.0'), help='Interface to bind')
    parser.add_argument('--port', type=int, default=int(os.getenv('PORT', '8000')), help='Port to listen on')
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), RequestHandler)
    print(f'Fieldwise is running at http://localhost:{args.port}')
    print(f'LAN access: http://{get_lan_ip()}:{args.port}')
    print('For public access, forward this port in your router and allow it through Windows Firewall.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopping Fieldwise server.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
