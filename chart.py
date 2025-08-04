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

        # ✅ Setup chart with off-white background
        off_white = '#f4f4f4'
        plt.figure(figsize=(10, 5), facecolor=off_white)
        ax = plt.gca()
        ax.set_facecolor(off_white)  # chart area background

        # ✅ Plot bars
        bars = plt.bar(labels, values, color='skyblue')

        # ✅ Add quantity labels on top of each bar
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(value),
                     ha='center', va='bottom', color='black', fontsize=10)

        # ✅ Add gridlines (auto)
        ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.6)
        ax.xaxis.grid(False)

        # ✅ Chart labels and ticks
        plt.xlabel("LOB", color='black')
        plt.ylabel("Quantity", color='black')
        plt.xticks(rotation=45, color='black')
        plt.yticks(color='black')

        # ✅ Save chart to image buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", facecolor=off_white)
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return jsonify({"image": f"data:image/png;base64,{encoded_image}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
