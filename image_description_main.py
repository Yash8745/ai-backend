from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load the processor and model outside the function for efficiency
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def describe_image(image_path: str) -> str:
    """
    Generates a description for an input image.

    Parameters:
    image_path (str): Path to the input image.

    Returns:
    str: Description of the image.
    """
    try:
        # Open the image using PIL
        image = Image.open(image_path)

        # Process the image and generate a description
        inputs = processor(image, return_tensors="pt")
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        
        return caption

    except Exception as e:
        # Log or return the error message
        print(f"Error describing the image: {e}")
        return "Error describing the image."
