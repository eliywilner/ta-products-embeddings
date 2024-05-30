import logging
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
from PIL import Image
import requests

logger = logging.getLogger(__name__)

def extract_embeddings(image_urls, texts, model, processor):
    try:
        logger.info("Starting to process images and texts for embeddings")
        images = [Image.open(requests.get(url, stream=True).raw) for url in image_urls]
        inputs = processor(text=texts, images=images, return_tensors="pt", padding=True)

        with torch.no_grad():
            outputs = model(**inputs)
            image_embeds = outputs.image_embeds
            text_embeds = outputs.text_embeds

        combined_embeds_list = []
        for image_embed, text_embed in zip(image_embeds, text_embeds):
            combined_embed = torch.cat((image_embed, text_embed), dim=0)
            combined_embed_numpy = combined_embed.cpu().numpy().flatten().astype(np.float16)
            combined_embeds_list.append(combined_embed_numpy)

        logger.info("Embeddings extracted successfully")
        return combined_embeds_list
    except Exception as e:
        logger.error(f"Error in extracting embeddings: {e}")
        raise
