from flask import Flask, render_template, request, jsonify
import socket

app = Flask(__name__)

def scan_ports(ip, start_port, end_port):
    results = []
    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((ip, port))
            results.append({'port': port, 'status': 'open'})
            s.close()
        except:
            results.append({'port': port, 'status': 'closed'})
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    ip = data['ip']
    start_port = int(data['start_port'])
    end_port = int(data['end_port'])

    result = scan_ports(ip, start_port, end_port)
    return jsonify({'ports': result})

if __name__ == '__main__':
    app.run(debug=True)
