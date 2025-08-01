from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/chart', methods=['POST'])
def chart():
    try:
        # Get incoming JSON data
        data = request.get_json()
        print("Received data:", data)  # ✅ Log input for debugging

        # Extract labels and values
        labels = data.get("labels", [])
        values = data.get("values", [])

        # Validate input
        if not labels or not values:
            print("❗ Missing 'labels' or 'values'")
            return jsonify({"error": "Missing labels or values"}), 400

        # Generate the bar chart
        plt.figure(figsize=(10, 5))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel("LOB")
        plt.ylabel("Quantity")
        plt.title("Invoice Quantity by LOB")
        plt.xticks(rotation=45)

        # Convert chart to base64 PNG
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        print("✅ Chart generated successfully.")
        return jsonify({"image": f"data:image/png;base64,{encoded_image}"})

    except Exception as e:
        # Catch and log any error
        print("🔥 Error generating chart:", str(e))
        return jsonify({"error": str(e)}), 500


# ✅ Make it publicly accessible on Railway
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
