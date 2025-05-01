# api/utils.py
import base64

def process_image_input(image_input):
    """Handle both URL and uploaded file input"""
    if isinstance(image_input, str) and image_input.startswith(("http://", "https://")):
        return {"type": "url", "value": image_input}
    else:
        # Handle InMemoryUploadedFile
        image_bytes = image_input.read()
        return {
            "type": "image",
            "value": base64.b64encode(image_bytes).decode("utf-8")
        }

def check_product_match(detected_class):
    """Check if detected class matches any product in the database"""
    from .models import Product
    return Product.objects.filter(name__iexact=detected_class).first()