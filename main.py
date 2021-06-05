from PyQt5 import QtWidgets, QtGui, QtCore
from mainwindow import Ui_Dialog
from qt_material import apply_stylesheet
from imager import imagify
import sys

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon("resources/icon.png"))
        self.setFixedSize(904,576)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.imagifybase = imagify()

        #  Setup My Creditation Image
        self.ui.mypfp.setPixmap(QtGui.QPixmap("resources/me.png").scaledToHeight(50))

        #  Load blocks into check box area
        preset_choice = self.ui.blockselectioncombobox.currentText()
        all_blocks = self.imagifybase.preset_block_list(preset_choice)

        self.block_label_list = []
        for block in all_blocks:
            block_label = QtWidgets.QCheckBox(f"{block['name']}")
            if block['bool']:
                block_label.setChecked(True)
            else:
                block_label.setChecked(False)
            self.block_label_list.append(block_label)
            self.ui.blockCheckboxArea.layout().addWidget(block_label)

        #  Load example image
        myImage = "resources/mallard.jpg"
        self.selected_file = myImage
        self.imagifybase.set_image(myImage)
        self.ui.OutputImageBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.OutputImageBox.setPixmap(QtGui.QPixmap(myImage).scaled(611, 481, aspectRatioMode=1))

        #  Setup Button Events
        self.ui.openfilebutton.clicked.connect(self.set_image) #  Select Image Button
        self.ui.convertbutton.clicked.connect(self.convert) #  Convert Image Button
        self.ui.blockselectioncombobox.currentTextChanged.connect(self.set_preset_blocklist)
        self.ui.SaveOutputTextButton.clicked.connect(self.save_text)
        self.ui.saveimagebutton.clicked.connect(self.save_image)

    def save_image(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image', '', "Image files (*.png)")
        print(fname)
        self.imagifybase.save_image(fname[0])

    def save_text(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Output', '', "Text file (*.txt)" )
        self.imagifybase.save_text(fname[0])

    def getfile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.png *.jpg)")
        return fname[0]

    def set_image(self):
        myImage = self.getfile()
        myImage = myImage if myImage != "" else "resources/mallard.jpg"
        self.selected_file = myImage
        self.imagifybase.set_image(myImage)
        self.ui.OutputImageBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.OutputImageBox.setPixmap(QtGui.QPixmap(myImage).scaled(611, 481, aspectRatioMode=1))
        print("I've been clicked!")

    def set_preset_blocklist(self):
        print("check!")
        preset_choice = self.ui.blockselectioncombobox.currentText()
        all_blocks = []
        for block in self.imagifybase.preset_block_list(preset_choice):
            if block['bool']:
                all_blocks.append(block['name'])
        for box in self.block_label_list:
            if box.text() in all_blocks:
                box.setChecked(True)
            else:
                box.setChecked(False)

    def get_blocklist(self):
        used_blocks = []
        for box in self.block_label_list:
            if box.isChecked() is True:
                used_blocks.append(box.text())
        return used_blocks



    def convert(self):
        self.imagifybase.width = self.ui.widthamount.value()
        self.imagifybase.height = self.ui.heightamount.value()
        self.imagifybase.method = self.ui.convertMethod.currentText()
        self.imagifybase.load_blocks("resources/All/*")
        print(f"Method: {self.imagifybase.method}")
        self.imagifybase.set_used_block_list(self.get_blocklist())
        self.imagifybase.set_image(self.selected_file)
        print(f"Image: {self.selected_file}")
        self.imagifybase.convert()
        pmap = QtGui.QPixmap("resources/Output.png")
        self.ui.OutputImageBox.setPixmap(pmap.scaled(611, 481,aspectRatioMode=1))
        self.ui.OutputText.setText(self.imagifybase.output_ingridients)




def main():
    """Setup the main window settings for PyQt5
        Also applies the modern theme for the program.
        Credits:
        - PIL Module
        - Pixelworlds Game for the Assets
        - marcel-goldschen-ohm for the Image Veiwer
        - color theif for dominant color method
        """
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    apply_stylesheet(app, theme='dark_cyan.xml')



    """Safely Shows and Exits the program"""
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()