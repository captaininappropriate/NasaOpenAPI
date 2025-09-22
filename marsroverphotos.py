from PyQt6.QtWidgets import (
    QDialog, 
    QHBoxLayout,
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
        rovers = ['Curiosity','Opportunity', 'Spirit']
        for rover in rovers:
            self.rover_list.addItem(rover)

        # camera list
        cameras = {
            "FHAZ": "Front Hazard Avoidance Camera",
            "RHAZ": "Rear Hazard Avoidance Camera",
            "MAST": "Mast Camera",
            "CHEMCAM": "Chemistry and Camera Complex",
            "MAHLI": "Mars Hand Lens Imager",
            "MARDI": "Mars Descent Imager",
            "NAVCAM": "Navigation Camera",
            "PANCAM": "Panoramic Camera",
            "MINITES": "Miniature Thermal Emission Spectrometer (Mini-TES)",
        }
        for value in cameras.values():
            self.camera_selection_list.addItem(value)

        layout.addWidget(self.calendar)
        layout.addWidget(self.rover_list)
        layout.addWidget(self.camera_selection_list)
        self.setLayout(layout)
        





