import logging
from PIL import Image
import requests
import hashlib

logger = logging.getLogger(__name__)

def compute_image_hash(image):
    try:
        logger.info("Computing hash for image")
        image_bytes = image.tobytes()
        hash_obj = hashlib.sha256(image_bytes)
        hash_digest = hash_obj.hexdigest()
        logger.info("Image hash computed successfully")
        return hash_digest
    except Exception as e:
        logger.error(f"Error computing image hash: {e}")
        raise

def load_image(url):
    try:
        logger.info(f"Loading image from URL: {url}")
        image = Image.open(requests.get(url, stream=True).raw)
        logger.info("Image loaded successfully")
        return image
    except Exception as e:
        logger.error(f"Error loading image from URL {url}: {e}")
        raise
