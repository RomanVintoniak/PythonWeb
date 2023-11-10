import os, secrets
from PIL import Image

from flask import current_app

def add_account_img(img_upload):
    random_hex = secrets.token_hex(8)
    filename = img_upload.filename
    
    ext_type = filename.split('.')[-1]
    storage_filename = random_hex + '.' + ext_type
    filepath = os.path.join(current_app.root_path, 'static\images', storage_filename)

    output_size = (200, 200)

    pic = Image.open(img_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename