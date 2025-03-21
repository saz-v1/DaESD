from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def resize_image(image, size=(800, 400), format='JPEG', quality=85):
    """
    Resizes an image to the specified dimensions and format
    
    Args:
        image: The image file to resize
        size: Tuple of (width, height)
        format: Output format (JPEG, PNG, etc.)
        quality: Image quality (1-100, JPEG only)
        
    Returns:
        A resized InMemoryUploadedFile
    """
    if image is None:
        return None
        
    # Open the image using Pillow
    img = Image.open(image)
    
    # Convert to RGB if necessary (for PNG with transparency)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize the image with aspect ratio preservation
    img.thumbnail(size, Image.LANCZOS)
    
    # Calculate padding to make the image exactly the target size
    width, height = img.size
    target_width, target_height = size
    
    # Create a new image with the target size and white background
    new_img = Image.new("RGB", size, (255, 255, 255))
    
    # Paste the resized image in the center
    paste_x = (target_width - width) // 2
    paste_y = (target_height - height) // 2
    new_img.paste(img, (paste_x, paste_y))
    
    # Save the image to an in-memory file
    output = BytesIO()
    new_img.save(output, format=format, quality=quality)
    output.seek(0)
    
    # Return a new InMemoryUploadedFile
    return InMemoryUploadedFile(
        output,
        'ImageField',
        f"{image.name.split('.')[0]}.jpg",
        f'image/{format.lower()}',
        sys.getsizeof(output),
        None
    ) 