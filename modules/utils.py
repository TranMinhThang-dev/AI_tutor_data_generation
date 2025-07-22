import base64
import fitz
from PIL import Image
from typing import List
import io

def image_to_base64(byte_image):
    image_base64 = base64.b64encode(byte_image).decode('utf-8')
    img_str = f"data:image/jpeg;base64,{image_base64}"
    return img_str

def pdf_pages_to_images(pdf_path, dpi=150) -> List[bytes]:  # Default to 300 DPI, which is print quality
    pdf_document = fitz.open(pdf_path)
    pages_as_images = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Calculate zoom factor based on desired DPI (default is 72 DPI)
        zoom_factor = dpi / 72
        
        # Create a higher resolution pixmap with the zoom factor
        matrix = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=matrix)
        
        # Convert the pixmap to a Pillow image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save the Pillow image in byte format
        img_byte_arr = io.BytesIO()
        # For better quality when saving as JPEG, you can specify quality
        img.save(img_byte_arr, format='JPEG', quality=95)
        pages_as_images.append(img_byte_arr.getvalue())

    pdf_document.close()
    return pages_as_images