from PyQt6.QtWidgets import (
    QDialog, 
    QHBoxLayout,
    QVBoxLayout,
    QCalendarWidget,
    QListWidget,
    QLabel,
    QPushButton,
)
import requests


class MarsRoverPhotosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Mars Rover Photos")
        #self.setMinimumSize(400, 600)

        # create layouts
        h_layout = QHBoxLayout()
        v_list_layout = QVBoxLayout() # QListQidget layout
        v_layout = QVBoxLayout()

        # create widgets
        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(200, 200)
        self.camera_selection_list = QListWidget()
        self.camera_selection_list.setFixedSize(320, 135)
        self.rover_list = QListWidget()
        self.rover_list.setFixedSize(320, 55)
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(100, 40)
        self.results_label = QLabel("Results will go here")
        
        # add items to the lists
        # rover list
        self.rover_list.addItems(['Curiosity','Opportunity', 'Spirit'])
        self.rover_list.currentItemChanged.connect(self.update_camera_list)

        # configure the QListWidget layout
        v_list_layout.addWidget(self.rover_list)
        v_list_layout.addWidget(self.camera_selection_list)

        # configure the primary horozontal layout
        h_layout.addWidget(self.calendar)
        h_layout.addLayout(v_list_layout)

        # confiugre the layouts
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.submit_button)
        v_layout.addWidget(self.results_label)
        self.setLayout(v_layout)
        
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





