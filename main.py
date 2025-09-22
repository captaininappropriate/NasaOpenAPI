from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QLabel,
)
import apod
import database
from apikeydialog import ApiKeyDialog
from marsroverphotos import MarsRoverPhotosDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NASA Open API")
        self.setMinimumSize(700, 500)

        # create widgets
        main_widget = QWidget()
        self.apod_image = QLabel()
        self.apod_image.setStyleSheet("border: 2px solid black;")
        self.apod_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.apod_title = QLabel()
        self.apod_title.setStyleSheet("border: 2px solid black;")
        self.apod_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apod_description = QLabel()
        self.apod_description.setStyleSheet("border: 2px solid black;")
        self.apod_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apod_description.setWordWrap(True)

        # configure layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.apod_image, 75)
        main_layout.addWidget(self.apod_title, 5)
        main_layout.addWidget(self.apod_description, 20)

        # set layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File") # type: ignore
        option_menu = menubar.addMenu("Options") # type: ignore

        # API Key action for file menu
        # api key action
        api_key_action = QAction("API Key", self)
        api_key_action.triggered.connect(self.open_api_key_dialog)
        file_menu.addAction(api_key_action) # type: ignore

        # close action
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action) # type: ignore

        # API Key action for option menu 
        # Mars rover action
        mars_photo_action = QAction("Mars Rover Photos", self)
        mars_photo_action.triggered.connect(self.open_mars_rover_photo_dialog)
        option_menu.addAction(mars_photo_action) # type: ignore

        # Status Bar to display status of API key
        self.statusBar().showMessage(self.get_api_key_status()) # type: ignore
        self.get_apod_data()

    # functions
    def get_api_key_status(self) -> str:
        """Check if API key exists and return appropriate status message."""
        api_key = database.load_api_key()
        if api_key:
            return "API key loaded"
        return "API key not set"

    def open_api_key_dialog(self):
        dialog = ApiKeyDialog()
        dialog.exec()

    def open_mars_rover_photo_dialog(self):
        dialog = MarsRoverPhotosDialog()
        dialog.exec()

    # get the data from the apod api and present onto the main screen
    def get_apod_data(self):
        api_key = database.load_api_key()
        if api_key:
            try:
                data = apod.get_apod_data(api_key)
                if data:
                    # set the title and description of the APOD image 
                    title = f"{data['title']}"
                    self.apod_title.setText(title)
                    explanation = f"{data['explanation']}"
                    self.apod_description.setText(explanation)
                    # extract the APOD image url and pass back to the apod module for processing
                    apod_image_url = data['image_url']
                    apod_image = apod.get_apod_image(apod_image_url)
                    # place the image in the label
                    self.apod_image.setPixmap(apod_image)
                    self.apod_image.setScaledContents(True) # scale when window is resized
            except ValueError as e:
                self.apod_description.setText(f"Error: {e}")
        else:
            self.apod_image.setText("Unable to load image")
            self.apod_description.setText("Unable to connect to NASA APOD API")


if __name__ == "__main__":
    database.init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()