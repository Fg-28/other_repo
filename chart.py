from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/chart', methods=['POST'])
def chart():
    try:
        data = request.get_json()
        labels = data.get("labels", [])
        values = data.get("values", [])

        if not labels or not values:
            return jsonify({"error": "Missing labels or values"}), 400

        # ✅ Setup chart with black background
        plt.figure(figsize=(10, 5), facecolor='black')
        ax = plt.gca()
        ax.set_facecolor('black')  # chart area background

        # ✅ Plot bars
        bars = plt.bar(labels, values, color='skyblue')

        # ✅ Add quantity labels on top of each bar
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(value),
                     ha='center', va='bottom', color='white', fontsize=10)

        # ✅ Clean look: remove chart title
        plt.xlabel("LOB", color='white')
        plt.ylabel("Quantity", color='white')
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')

        # ✅ Save to image
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", facecolor='black')  # also save with black bg
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return jsonify({"image": f"data:image/png;base64,{encoded_image}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
