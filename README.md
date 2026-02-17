# Images Microservice

## Description

This microservice retrieves random images by category from a local SQLite database.

It allows clients to:

- Request a random image from a specific category
- Retrieve a list of available categories
- Verify service health

The service downloads images once (via Pexels API), stores them locally, and serves them from a static directory.  
It does NOT rely on external APIs at runtime.

---

## Developer

Philip Gadsden, Hunter Havice

---

## Technology Stack

- Python
- Flask
- SQLite
- Pillow (image processing)
- Requests (image download script)
- Local static image storage

---

## Communication Contract

### How to Request Data

#### Retrieve a Random Image

**Endpoint:**  
GET /image

**Query Parameter:**

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| category  | string | Yes      | Category of image to retrieve |

**Example Request (Browser):**

http://localhost:5005/image?category=animals

**Example Request (Python):**

```python
import requests

url = "http://localhost:5005/image"
params = {"category": "animals"}

response = requests.get(url, params=params)
print(response.json())
```

---

#### Retrieve All Categories

**Endpoint:**  
GET /categories  

No parameters required.

**Example Request:**

http://localhost:5005/categories

---

### How to Receive Data

Response format: JSON

#### Successful Image Response

```json
{
  "category": "animals",
  "image_path": "/static/images/animals/animals_3.jpg"
}
```

To view the image, prepend the service base URL:

```
http://localhost:5005/static/images/animals/animals_3.jpg
```

---

#### Successful Categories Response

```json
{
  "categories": [
    "animals",
    "city",
    "food",
    "nature",
    "space"
  ]
}
```

---

#### Health Response

```json
{
  "status": "ok"
}
```

---

### Error Responses

#### Missing Category Parameter (400)

```json
{
  "error": "category parameter required"
}
```

#### Category Not Found (404)

```json
{
  "error": "No images found for that category"
}
```

---

## Endpoints

GET /health  
GET /categories  
GET /image?category=<category>  

---

## Running the Microservice

### 1. Install Dependencies

```
pip install -r requirements.txt
```

---

### 2. Download Images (Optional Setup Step)

Set your Pexels API key:

```
export PEXELS_API_KEY=your_key_here
```

Run:

```
python download_images.py
```

This downloads images into:

```
static/images/<category>/
```

---

### 3. Initialize Database

Run:

```
python import_images.py
```

This creates `images.db` and indexes all images by category.

---

### 4. Start the Service

```
python app.py
```

The service will run at:

```
http://localhost:5005
```

---

## Example Requests

Random animals image:

```
http://localhost:5005/image?category=animals
```

List categories:

```
http://localhost:5005/categories
```

Health check:

```
http://localhost:5005/health
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 400  | Missing category parameter |
| 404  | Category not found |
| 500  | Internal server error |

---

## UML Sequence Diagram
```
Client                          Images Microservice
  |                                      |
  | GET /image?category=animals          |
  |------------------------------------->|
  |                                      | Query SQLite DB
  |                                      | ORDER BY RANDOM()
  |                                      | LIMIT 1
  |                                      |
  | 200 OK                               |
  | {category, image_path}               |
  |<-------------------------------------|
```
---

## Architecture Overview

SQLite stores:
- category
- file_path

Images are stored locally in:

```
static/images/<category>/
```

Flask serves static files automatically.

The database acts as an index that maps categories to image file paths.
The filesystem stores the actual image data.

---

## License Notice

Images were downloaded via the Pexels API under the Pexels Free License.