import random

import requests

BASE_URL = "http://localhost:5005"

def main():
    # 1) Get categories
    print("GET /categories")
    r = requests.get(f"{BASE_URL}/categories", timeout=5)
    print("Status:", r.status_code)

    if r.status_code != 200:
        print("Body:", r.text)
        return

    data = r.json()
    print("JSON:", data)

    categories = data.get("categories", [])
    if not categories:
        print("No categories returned. Database may be empty.")
        return

    category = categories[random.randint(0, len(categories)-1)]
    print(f"\nUsing category: {category}")

    # 2) Get random image for that category
    print("GET /image?category=...")
    r = requests.get(f"{BASE_URL}/image", params={"category": category}, timeout=5)
    print("Status:", r.status_code)

    if r.status_code != 200:
        print("Body:", r.text)
        return

    img_data = r.json()
    print("JSON:", img_data)

    # 3) construct a URL you can paste into the browser
    image_path = img_data.get("image_path")
    if not image_path:
        print("No image_path in response.")
        return

    if image_path.startswith("/"):
        image_url = BASE_URL + image_path
    else:
        image_url = image_path

    print("\nPaste this into your browser to view the image:")
    print(image_url)

if __name__ == "__main__":
    main()