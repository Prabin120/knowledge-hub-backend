import base64
import os
import aiofiles

async def save_base64_image(base64_str: str, file_name: str, save_dir: str = "images") -> str:
    """
    Decodes a base64 image string and saves it to the filesystem asynchronously.

    Args:
        base64_str (str): The base64-encoded image string (may include data URL prefix).
        file_name (str): The name to save the image as (should include extension, e.g., 'image.png').
        save_dir (str): Directory to save the image in. Defaults to 'images'.

    Returns:
        str: The full path to the saved image.
    """
    os.makedirs(save_dir, exist_ok=True)
    if "," in base64_str:
        base64_str = base64_str.split(",", 1)[1]
    try:
        image_data = base64.b64decode(base64_str)
    except Exception as e:
        raise ValueError("Invalid base64 string") from e
    file_path = os.path.join(save_dir, file_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(image_data)
    return file_path

async def get_image_from_base64(base64_str: str):
    if not base64_str:
        return None
    try:
        image = base64.b64decode(base64_str)
    except Exception as e:
        raise ValueError("Invalid base64 string") from e
    return image
