from django.apps import AppConfig
from ultralytics import YOLO

class CapstoneUiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capstone_UI_app'
    
    model = None
    
    def ready(self):
        CapstoneUiAppConfig.model = YOLO('capstone_UI_app/best.pt')
        
        # Run batched inference on a list of images
        results = CapstoneUiAppConfig.model(['media/images/565Neg.jpg'])  # return a list of Results objects
        
        # Process results list
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            result.show()  # display to screen
            result.save(filename='result.jpg')  # save to disk



