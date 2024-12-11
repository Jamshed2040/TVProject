from PyQt6 import QtWidgets, QtGui
from remote_design import Ui_MainWindow
from project_television import Television
import os


class TVRemoteApp(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        """
        Initialize the TV Remote app. Set up ui library and
        validate the images in case there is an error
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """Initialize Television class"""
        self.tv = Television()

        """Validate images folder and files"""
        images_folder = "images"
        if not os.path.exists(images_folder):
            QtWidgets.QMessageBox.critical(self, "Error", f"Folder '{images_folder}' not found. Please create the folder and add channel images.")
            self.channel_images = []
        else:
            self.channel_images = [
                os.path.join(images_folder, f"channel{i}.png") for i in range(1, 7)
            ]
            """Validate individual files"""
            missing_files = [
                image for image in self.channel_images if not os.path.exists(image)
            ]
            if missing_files:
                missing_list = "\n".join(missing_files)
                QtWidgets.QMessageBox.warning(self, "Missing Files", f"The following files are missing:\n{missing_list}")

        """Add a QLabel to display the channel image"""
        self.channel_label = QtWidgets.QLabel(self)
        self.channel_label.setGeometry(100, 50, 250, 150)  # adjust position and size
        self.channel_label.setScaledContents(True)  # scale image to fit label
        self.channel_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        """Adjust the volume progress bar to match the image's width"""
        self.ui.progressBar.setGeometry(100, 210, 250, 20)  # match QLabel width and position

        """ Connect buttons to the respective functions"""
        self.ui.pushButton.clicked.connect(self.toggle_power)
        self.ui.volume_up_2.clicked.connect(self.toggle_mute)
        self.ui.volume_up_7.clicked.connect(self.channel_up)
        self.ui.volume_up_8.clicked.connect(self.channel_down)
        self.ui.volume_up_9.clicked.connect(self.volume_up)
        self.ui.volume_up_10.clicked.connect(self.volume_down)

        """ Create a function for each channel and connect the buttons with respective channels"""
        self.ui.volume_up.clicked.connect(lambda: self.set_channel(1))
        self.ui.volume_up_5.clicked.connect(lambda: self.set_channel(2))
        self.ui.volume_up_3.clicked.connect(lambda: self.set_channel(3))
        self.ui.volume_up_4.clicked.connect(lambda: self.set_channel(4))
        self.ui.volume_up_11.clicked.connect(lambda: self.set_channel(5))
        self.ui.volume_up_6.clicked.connect(lambda: self.set_channel(6))

        """Update the UI interface when the buttons are clicked"""
        self.update_ui()

    def toggle_power(self) -> None:
        """Turn the tv on/off and update the ui"""
        self.tv.power()
        self.update_ui()

    def toggle_mute(self) -> None:
        """mute/unmute and update the ui"""
        self.tv.mute()
        self.update_ui()

    def channel_up(self) -> None:
        """Change the tv channel to the next and update ui.
        Go to the first channel when the max is reached"""
        self.tv.channel_up()
        self.update_ui()

    def channel_down(self) -> None:
        """Change the tv channel to the previous and update ui.
        Go to the last channel when the min is reached"""
        self.tv.channel_down()
        self.update_ui()

    def volume_up(self) -> None:
        """Increase the tv volume and update ui if the tv is muted unmute it"""
        self.tv.volume_up()
        self.update_ui()

    def volume_down(self) -> None:
        """Decrease the tv volume and update the ui if the tv is muted unmute it"""
        self.tv.volume_down()
        self.update_ui()

    def set_channel(self, channel) -> None:
        """Set the tv to a specific channel and update the ui"""
        self.tv.set_channel(channel)
        self.update_ui()

    def update_ui(self) -> None:
        """Update the UI elements based on the current tv state.
        Handles power, mute, volume, channel display"""
        # Handle TV off state
        if not self.tv.get_status():
            self.ui.progressBar.setValue(0)
            self.ui.progressBar.setEnabled(False)
            self.ui.volume_up_2.setText("🔇")
            self.ui.volume_up_7.setEnabled(False)
            self.ui.volume_up_8.setEnabled(False)
            self.ui.volume_up_9.setEnabled(False)
            self.ui.volume_up_10.setEnabled(False)
            self.channel_label.clear()  # clear the channel image when the TV is off
        else:
            """handle tv on state"""
            self.ui.progressBar.setEnabled(True)
            self.ui.progressBar.setValue(int(self.tv.get_volume() * (100 / Television.MAX_VOLUME)))
            self.ui.volume_up_2.setText("🔊" if not self.tv.is_muted() else "🔇")
            self.ui.volume_up_7.setEnabled(True)
            self.ui.volume_up_8.setEnabled(True)

            """disable volume controls and progress bar if muted"""
            if self.tv.is_muted():
                self.ui.progressBar.setEnabled(False)
                self.ui.volume_up_9.setEnabled(False)
                self.ui.volume_up_10.setEnabled(False)
            else:
                self.ui.volume_up_9.setEnabled(True)
                self.ui.volume_up_10.setEnabled(True)

            """update the channel image"""
            current_channel = self.tv.get_channel()
            if 1 <= current_channel <= len(self.channel_images):
                image_path = self.channel_images[current_channel - 1]
                if os.path.exists(image_path):
                    pixmap = QtGui.QPixmap(image_path)
                    self.channel_label.setPixmap(pixmap)
                else:
                    self.channel_label.clear()  # clear label if image not found
            else:
                self.channel_label.clear()

        """keep static button texts for channels and volume"""
        self.ui.volume_up_9.setText("+")
        self.ui.volume_up_10.setText("-")
        self.ui.volume_up_7.setText("^")
        self.ui.volume_up_8.setText("v")
        self.ui.volume_up.setText("1")
        self.ui.volume_up_5.setText("2")
        self.ui.volume_up_3.setText("3")
        self.ui.volume_up_4.setText("4")
        self.ui.volume_up_11.setText("5")
        self.ui.volume_up_6.setText("6")

        """Show current channel feedback in a tooltip"""
        self.ui.pushButton.setText(f"Power ({'On' if self.tv.get_status() else 'Off'})")
        self.ui.volume_up_2.setToolTip(f"Channel: {self.tv.get_channel()}")


if __name__ == "__main__":
    import sys
    from PyQt6 import QtCore

    app = QtWidgets.QApplication(sys.argv)
    main_window = TVRemoteApp()
    main_window.show()
    sys.exit(app.exec())
