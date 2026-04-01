from flask import Flask, jsonify
import time

app = Flask(__name__)

start_time = time.time()

@app.route("/health")
def health():
   print("Endpoint /health diakses!") 
   
   return jsonify({
       "nama": "NAMA KAMU",
       "nrp": "NRP KAMU",
       "status": "Running",
       "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
       "uptime": int(time.time() - start_time)
   })

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
