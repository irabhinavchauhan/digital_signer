# signer_engine.py
import fitz  # PyMuPDF
from datetime import datetime
from PIL import Image
import os

def sign_pdf(input_path, output_path, log_path, audit_path):
    doc = fitz.open(input_path)

    signature_image_path = "assets/signature_stamp.png"
    if not os.path.exists(signature_image_path):
        raise FileNotFoundError(f"Signature image not found at {signature_image_path}")

    img = Image.open(signature_image_path)
    width, height = img.size
    width, height = width / 3, height / 3

    sig_image_data = open(signature_image_path, "rb").read()

    for page in doc:
        rect = fitz.Rect(40, 740, 40 + width, 740 + height)
        page.insert_image(rect, stream=sig_image_data)

    doc.save(output_path)

    with open(log_path, "a") as log:
        log.write(f"{datetime.now()} - Signed {input_path} -> {output_path}\n")

    with open(audit_path, "a") as audit:
        audit.write(f"{datetime.now()},{input_path},{output_path},Signed\n")
