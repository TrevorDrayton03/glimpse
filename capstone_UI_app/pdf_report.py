from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from PIL import Image
from datetime import datetime
import os

def generate_pdf_report(results_data, pdf_path):
    c = Canvas(pdf_path, pagesize=letter)
    total_pages = len(results_data)  # Assume you know the total number of pages ahead of time or calculate it
    page_number = 1

    # for i in range(total_pages):
    #     c.drawString(100, 750, f"Content for page {i + 1}")
    #     page_num_text = f"{i + 1} / {total_pages}"
    #     c.drawString(500, 20, page_num_text)  
    #     c.showPage()

    for image_data in results_data:
        page_num_text = f"{page_number} / {total_pages}"
        c.drawString(500, 20, page_num_text)  
        image_path_org = image_data['original_path']
        image_path_pre = image_data['processed_path']
        # patient_id = image_data['patient_id']
        # pre_process_steps = image_data['pre_process_steps']
        # confidence = image_data['']
        annotated_image_path = image_data["annotated_image_path"]

        current_date = datetime.now().strftime("%Y-%m-%d")

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 750, "GLIMPSE Report")
        c.drawString(100, 730, f"Date: {current_date}")
        # c.drawString(100, 710, f"Patient ID: {patient_id}")

        display_image_and_text(c, image_path_org, 100, 350, "Original Image")
        display_image_and_text(c, image_path_pre, 350, 350, "Pre-Processed Image")

        c.setFont("Helvetica", 12)
        # c.drawString(100, 500, f"Glaucoma Detection Confidence Level: {confidence}")
        # c.drawString(100, 480, f"Pre-Processing Steps Added: {pre_process_steps}")
        # c.drawImage(annotated_image_path, 100, 300, width=200, height=200)  
        display_image_and_text(c, annotated_image_path, 100, 600, "Annotated Image")
        
        c.showPage()
        
        page_number += 1
        print(annotated_image_path)
        delete_processed_image(annotated_image_path)

    c.save()

def display_image_and_text(c, image_path, x, y, label):
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y + 20, label)
    with Image.open(image_path) as img:
        width, height = img.size
        desired_width = 200
        scale_factor = desired_width / width
        scaled_height = scale_factor * height
        c.drawImage(image_path, x, y - scaled_height, width=desired_width, height=scaled_height, mask='auto')

def delete_processed_image(image_path):
    try:
        os.remove(image_path)
    except OSError as e:
        print(f"Error deleting file {image_path}: {e}")