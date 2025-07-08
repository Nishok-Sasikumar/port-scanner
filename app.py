from flask import Flask, render_template, request, jsonify
import socket
import ipaddress

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    ip = data.get("ip")
    start_port = int(data.get("start_port", 0))
    end_port = int(data.get("end_port", 0))

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400

    result = []
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((ip, port))
            status = "open"
        except:
            status = "closed"
        finally:
            s.close()
        result.append({"port": port, "status": status})
    return jsonify({"ports": result})

if __name__ == "__main__":
    app.run(debug=True)
