# app.py
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/chart', methods=['POST'])
def generate_chart():
    data = request.json

    labels = data.get("labels", [])
    values = data.get("values", [])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values, color='skyblue')
    ax.set_title('Previous Month Quantity by LOB')
    ax.set_ylabel('Quantity')
    ax.set_xlabel('LOB')

    # Output to bytes
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({
        "image": f"data:image/png;base64,{image_base64}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

