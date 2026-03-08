import random
import requests

BASE_URL = "http://localhost:5005"


def get_categories():
    """Fetch available image categories from the microservice."""
    print("GET /categories")
    response = requests.get(f"{BASE_URL}/categories", timeout=5)
    print("Status:", response.status_code)
    if response.status_code != 200:
        print("Body:", response.text)
        return []
    categories_data = response.json()
    print("JSON:", categories_data)
    return categories_data.get("categories", [])


def get_random_image(category):
    """Fetch a random image for the given category."""
    print(f"\nUsing category: {category}")
    print("GET /image?category=...")
    response = requests.get(
        f"{BASE_URL}/image", params={"category": category}, timeout=5
    )
    print("Status:", response.status_code)
    if response.status_code != 200:
        print("Body:", response.text)
        return None
    image_data = response.json()
    print("JSON:", image_data)
    return image_data


def print_image_url(image_data):
    """Construct and print the full image URL."""
    image_path = image_data.get("image_path")
    if not image_path:
        print("No image_path in response.")
        return
    if image_path.startswith("/"):
        image_url = BASE_URL + image_path
    else:
        image_url = image_path
    print("\nPaste this into your browser to view the image:")
    print(image_url)


def main():
    categories = get_categories()
    if not categories:
        print("No categories returned. Database may be empty.")
        return
    category = categories[random.randint(0, len(categories) - 1)]
    image_data = get_random_image(category)
    if image_data:
        print_image_url(image_data)


if __name__ == "__main__":
    main()