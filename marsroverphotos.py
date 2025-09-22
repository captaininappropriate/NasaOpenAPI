from PyQt6.QtWidgets import (
    QDialog, 
    QHBoxLayout,
    QVBoxLayout,
    QCalendarWidget,
    QListWidget,
    QLabel,
)
import requests


class MarsRoverPhotosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Mars Rover Photos")
        self.setMinimumSize(400, 400)

        # create layout
        layout = QHBoxLayout()

        # create widgets
        self.calendar = QCalendarWidget()
        self.camera_selection_list = QListWidget()
        self.rover_list = QListWidget()
        
        # add items to the lists
        # rover list
        self.rover_list.addItems(['Curiosity','Opportunity', 'Spirit'])
        self.rover_list.currentItemChanged.connect(self.update_camera_list)

        layout.addWidget(self.calendar)
        layout.addWidget(self.rover_list)
        layout.addWidget(self.camera_selection_list)
        self.setLayout(layout)
        
        # initial list of items
        self.update_camera_list()

    def update_camera_list(self):
        self.camera_selection_list.clear()

        # get the current rover
        current = self.rover_list.currentItem()

        if not current:
            return

        # curiosity camera list
        curiosity_cameras = {
            "FHAZ": "Front Hazard Avoidance Camera",
            "RHAZ": "Rear Hazard Avoidance Camera",
            "MAST": "Mast Camera",
            "CHEMCAM": "Chemistry and Camera Complex",
            "MAHLI": "Mars Hand Lens Imager",
            "MARDI": "Mars Descent Imager",
            "NAVCAM": "Navigation Camera",
        }

        # opportunity & spirit camera list
        opportunity_spirit_cameras = {
            "FHAZ": "Front Hazard Avoidance Camera",
            "RHAZ": "Rear Hazard Avoidance Camera",
            "NAVCAM": "Navigation Camera",
            "PANCAM": "Panoramic Camera",
            "MINITES": "Miniature Thermal Emission Spectrometer (Mini-TES)",
        }
        
        # select appropriate camera list
        # curiosity
        if current.text() == "Curiosity":
            for value in curiosity_cameras.values():
                self.camera_selection_list.addItem(value)
        else:  # "opportunity & spirit
            for value in opportunity_spirit_cameras.values():
                self.camera_selection_list.addItem(value)





