import logging
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from app.models import EmbeddingRequest
from app.utils import compute_image_hash, load_image
from app.embeddings import extract_embeddings
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load the model and processor once at startup
logger.info("Loading model and processor...")
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
logger.info("Model and processor loaded successfully")

@app.post("/embed/")
async def embed_data(request: EmbeddingRequest):
    try:
        logger.info(f"Received request with {len(request.pairs)} pairs")
        embeddings = []

        for pair in request.pairs:
            logger.info(f"Processing pair with title: {pair.product_title}")
            image_urls = pair.product_image_url
            texts = [pair.product_title] * len(image_urls)

            pair_embeddings = extract_embeddings(image_urls, texts, model, processor)
            embeddings.extend(pair_embeddings)

        response = []
        for idx, (embedding, pair) in enumerate(zip(embeddings, request.pairs)):
            image_hash = compute_image_hash(load_image(pair.product_image_url[0]))
            response.append({
                "product_image_url": pair.product_image_url,
                "product_title": pair.product_title,
                "embedding": embedding.tolist(),
                "image_hash": image_hash
            })
        
        logger.info("Embeddings successfully generated")
        return {"results": response}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
