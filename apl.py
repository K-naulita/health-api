from flask import Flask, jsonify
import time

app = Flask(__name__)

start_time = time.time()

@app.route("/health")
def health():
    return jsonify({
        "nama": "KARTIKA NANA NAULITA",
        "nrp": "5025241021",
        "status": "CI/CD WORKING",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "uptime": int(time.time() - start_time)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
