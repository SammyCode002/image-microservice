import sqlite3
from flask import Flask, jsonify, request

DB_PATH = "images.db"

app = Flask(__name__)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/categories")
def categories():
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT category FROM images ORDER BY category"
    ).fetchall()
    conn.close()

    return jsonify({"categories": [r["category"] for r in rows]})


@app.get("/image")
def random_image():
    category = request.args.get("category")

    if not category:
        return jsonify({"error": "category parameter required"}), 400

    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM images WHERE category=? ORDER BY RANDOM() LIMIT 1",
        (category,)
    ).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "No images found for that category"}), 404

    image_path = "/" + row["file_path"]

    return jsonify({
        "category": category,
        "image_path": image_path
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)