from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from datetime import datetime
import os

def generate_pdf_report(results_data, pdf_path):
    c = Canvas(pdf_path, pagesize=letter)
    total_pages = len(results_data)
    page_number = 1

    for image_data in results_data:
        page_num_text = f"{page_number} / {total_pages}"
        c.drawString(500, 20, page_num_text)
        image_path_org = image_data['original_path']
        image_path_pre = image_data['processed_path']
        annotated_image_path = image_data["annotated_image_path"]
        # resnet_prediction = image_data["resnet_prediction"]
        # resnet_probabilities = image_data["resnet_probabilities"]
        final_prediction = image_data["final_prediction"]
        # greater_confidence_value = image_data["greater_confidence_value"]   
        yolo_confidence = image_data["yolo_confidence"]
        # eye = image_data["eye"]
        image_name = image_data["image_name"]

        current_date = datetime.now().strftime("%Y-%m-%d")
        # eye_text = "Left" if eye == 0 else "Right"
        image_name_without_prefix = image_name.split('/')[-1]
        yolo_confidence_percentage = round(yolo_confidence * 100)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 750, "GLIMPSE Report")
        c.drawString(100, 730, f"Date: {current_date}")

        # Original, Pre-Processed, and Annotated Image display
        display_image_and_text(c, image_path_org, 100, 560, "Original Image")
        display_image_and_text(c, image_path_pre, 350, 560, "Pre-Processed Image")
        display_image_and_text(c, annotated_image_path, 100, 360, "YOLOv8")
        # c.drawString(350, 420, "ResNet18 Prediction")

        # Adding ResNet Prediction and Final Prediction text
        c.setFont("Helvetica", 12)
        # c.drawString(350, 390, f"Prediction: {resnet_prediction}")
        # c.drawString(350, 370, f"Confidence Level: {resnet_probabilities}")
        c.drawString(175, 680, "Prediction:")
        c.drawString(175, 660, "Confidence Level:")
        c.drawString(175, 640, "File:")
        # c.drawString(175, 620, "Eye:")
        c.drawString(325, 680, f"{final_prediction}")
        c.drawString(325, 660, f"{yolo_confidence_percentage}%")
        c.drawString(325, 640, image_name_without_prefix)
        # c.drawString(325, 620, eye_text)

        c.showPage()
        page_number += 1

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
