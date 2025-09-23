from PyQt6.QtGui import QPixmap, QImage
import requests


def get_apod_data(key: str):
    """
    
    """
    api_key = key
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # extract and return required details
    apod_details = {
        "title": data.get("title"),
        "explanation": data.get("explanation"),
        "image_url": data.get("url")
    }
    return apod_details 

def get_apod_image(url: str) -> QPixmap:
        """
        
        """
        # Download image data
        response = requests.get(url)
        response.raise_for_status()  # raise an error if download fails
        data = response.content

        # Convert to QImage
        image = QImage.fromData(data)
        if image.isNull():
            raise ValueError("Failed to load image from URL")
        
        # Convert QImage to QPixmap
        return QPixmap.fromImage(image)