from django.apps import AppConfig
from ultralytics import YOLO

import pandas as pd
import numpy as np
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib import styles
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Table, Spacer, TableStyle
from PIL import Image
from datetime import datetime

class CapstoneUiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capstone_UI_app'
    
    model = None
    
    def ready(self):
        CapstoneUiAppConfig.model = YOLO('capstone_UI_app/best.pt')
        
        # # Run batched inference on a list of images
        # results = CapstoneUiAppConfig.model(['media/images/565Neg.jpg'])  # return a list of Results objects
        
        # Process results list
        # for result in results:
        #     boxes = result.boxes  # Boxes object for bounding box outputs
        #     masks = result.masks  # Masks object for segmentation masks outputs
        #     keypoints = result.keypoints  # Keypoints object for pose outputs
        #     probs = result.probs  # Probs object for classification outputs
        #     result.show()  # display to screen
        #     result.save(filename='results/result.jpg')  # save to disk
           

        # pdf_path = 'results/GLIMPSE.pdf'
        # image_path_org = 'results/result.jpg'
        # image_path_pre = 'results/result.jpg'

        # current_date = datetime.now().strftime("%Y-%m-%d")
        # c = Canvas(pdf_path, pagesize=letter)

        # bold_style = styles.getSampleStyleSheet()["Heading1"]
        # bold_style.fontName = "Helvetica-Bold"

        # # Title of report
        # c.drawString(100, 750, "GLIMPSE Report")

        # # Add the date, file name, and patient id
        # date_x = letter[0] - 200
        # date_y = letter[1] - 30
        # c.drawString(date_x, date_y, f"Date: {current_date}")

        # file_x = date_x
        # file_y = date_y - 15
        # c.drawString(file_x, file_y, f"Original Image File: {image_path_org}")

        # patient_id = '12345'
        # patient_x = date_x
        # patient_y = file_y - 15
        # c.drawString(patient_x, patient_y, f"Patient ID: {patient_id}")

        # # Get the images
        # image1 = Image.open(image_path_org)
        # original_width, original_height = image1.size
        # desired_width = 200
        # scale_factor = desired_width / original_width
        # scaled_height = scale_factor * original_height

        # image2 = Image.open(image_path_pre)
        # pre_width, pre_height = image2.size
        # scale_factor_pre = desired_width / pre_width
        # scaled_height_pre = scale_factor_pre * pre_height

        # # Display the original image
        # original_label = "Original Image"
        # original_image_x = 100
        # original_image_y = 550
        # c.setFont(bold_style.fontName, bold_style.fontSize)
        # c.drawString(original_image_x, original_image_y + 150, f"{original_label}")
        # c.drawImage(image_path_org, original_image_x, original_image_y, width=desired_width, height=scaled_height)

        # # Display the pre-processed image
        # pre_label = "Pre-Processed Image"
        # pre_image_x = original_image_x + 250
        # pre_image_y = original_image_y
        # c.setFont(bold_style.fontName, bold_style.fontSize)
        # c.drawString(pre_image_x, pre_image_y + 150, f"{pre_label}")
        # c.drawImage(image_path_pre, pre_image_x, pre_image_y, width=desired_width, height=scaled_height_pre)

        # c.setFont("Helvetica", 12)

        # pre_process_steps = "1,2,3,4"
        # confidence = "" + "%"
        # c.drawString(original_image_x, original_image_y - 25, f"Glaucoma Detection Confidence Level: {confidence}")
        # c.drawString(pre_image_x, pre_image_y - 25, f"Pre-Processing Steps Added: {pre_process_steps}")
        # c.save()


        # df = pd.DataFrame(np.random.randn(5,4), columns=['one', 'two', 'three', 'four'],
        #           index=['a','b','c','d','e'])

        # df = df.reset_index()
        # df = df.rename(columns={"index": ""})
        # data = [df.columns.to_list()] + df.values.tolist()
        # table = Table(data)
        # table.setStyle(TableStyle([
        #     ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        #     ('BOX', (0,0), (-1,-1), 0.25, colors.black)
        # ]))
        
        # story = [Paragraph("GLIMPSE Report", getSampleStyleSheet()['Heading1']),
        #  Spacer(1,20),
        #  table]

        # c = Canvas('GLIMPSE.pdf')
        # f = Frame(inch, inch, 6 * inch, 9 * inch)
        # f.addFromList(story, c)
        # c.save()


