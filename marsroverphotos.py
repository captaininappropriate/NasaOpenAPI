from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QCalendarWidget,
    QListWidget,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import QDate
import requests
from database import load_api_key


class MarsRoverPhotosDialog(QDialog):
    """
    
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Mars Rover Photos")

        # Dictionary for rover camera QListWidget
        self.rover_camera_dict = {
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

        # Layouts
        v_layout = QVBoxLayout(self)
        v_list_layout = QVBoxLayout(self)
        h_layout = QHBoxLayout(self)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        h_layout.addWidget(self.calendar)

        # Rover list
        self.rover_list = QListWidget()
        self.rover_list.addItems(["Curiosity", "Opportunity", "Spirit"])
        v_list_layout.addWidget(self.rover_list)

        # Camera list
        self.camera_list = QListWidget()
        v_list_layout.addWidget(self.camera_list)

        # configure layouts
        h_layout.addLayout(v_list_layout)
        v_layout.addLayout(h_layout)

        # Button to confirm selection
        self.confirm_btn = QPushButton("Confirm Selection")
        v_layout.addWidget(self.confirm_btn)

        # Label to show result
        self.result_label = QLabel("Select date and items...")
        v_layout.addWidget(self.result_label)

        self.setLayout(v_layout)

        # Signals
        self.rover_list.currentItemChanged.connect(self.update_camera_list)
        self.confirm_btn.clicked.connect(self.get_selection)

    def update_camera_list(self):
        """Update second QListWidget based on first list selection."""
        self.camera_list.clear()
        rover = self.rover_list.currentItem()
        if not rover:
            return

        if rover.text() == "Curiosity":
            keys = ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"]
        else:  # Opportunity or Spirit
            keys = ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"]

        # Store key in QListWidget item data
        for key in keys:
            self.camera_list.addItem(self.rover_camera_dict[key])

    def get_selection(self):
        """Get selected values and call NASA API."""
        date: QDate = self.calendar.selectedDate()  # type: ignore
        rover_list_item = self.rover_list.currentItem()
        camera_list_item = self.camera_list.currentItem()

        if not rover_list_item or not camera_list_item:
            self.result_label.setText("Please select items from both lists.")
            return

        # Find dictionary key for selected value in list2
        value = camera_list_item.text()
        key = [k for k, v in self.rover_camera_dict.items() if v == value][0]

        # Get the selected rover
        rovers = self.rover_list.selectedItems()
        if rovers:
            rover = rovers[0]  # Get the first selected item
            rover_name = rover.text()

        camera = self.rover_camera_dict[key]
        date_str = date.toString("yyyy-MM-dd")

        # Build NASA API URL
        api_key = load_api_key()
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?earth_date={date_str}&api_key={api_key}"

        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            photos = data.get("photos", [])
            if photos:

                result = f"Found {len(photos)} photos. Example ID: {photos[0]['id']}"
            else:
                result = "No photos found for this selection."

        except Exception as e:
            result = f"API request failed: {e}"

        self.result_label.setText(result)
        print(result)
