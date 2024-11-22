from PIL import Image, ImageChops

# Open the image
image_path = "fisch.png"  # Replace with your image file
image = Image.open(image_path)

# Ensure the image is in RGBA mode for processing
if image.mode != "RGBA":
    image = image.convert("RGBA")

# Auto-crop to remove transparency or uniform borders
def trim(image):
    # Create a solid background (white) to compare against
    bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
    # Calculate the difference between the image and the background
    diff = ImageChops.difference(image, bg)
    # Get the bounding box of non-white content
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image

# Remove transparency by flattening it against a white background
def remove_transparency(image):
    if image.mode in ("RGBA", "LA"):
        # Create a white background
        bg = Image.new("RGB", image.size, (255, 255, 255))
        # Merge the image with the background
        return Image.alpha_composite(bg.convert("RGBA"), image).convert("RGB")
    return image.convert("RGB")  # Ensure no transparency remains

# Trim borders
trimmed_image = trim(image)

# Remove transparency and save as JPEG
output_image = remove_transparency(trimmed_image)
output_path = "trimmed_image.jpg"
output_image.save(output_path, "JPEG", quality=95)

print(f"Trimmed and saved image as: {output_path}")
