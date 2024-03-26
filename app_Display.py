from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal
# Supposons que "algo" est le module contenant "algorithmManager"
from algo import algorithmManager as algorithm
import sys


# Custom widget class containing a button and a label
class ButtonWithLabel(QWidget):
    def __init__(self, button_text, label_text):
        super().__init__()

        layout = QVBoxLayout()
        
        self.label = QLabel(label_text)

        self.button = QPushButton(button_text)
        self.button.setFixedSize(20, 20)
        if button_text == "1":
            self.button.setStyleSheet("QPushButton { background-color: green; border: 2px solid red; }")
        else:
            self.button.setStyleSheet("QPushButton { border: 2px solid blue; }")
        
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        self.setLayout(layout)

# Main window class
class MainWindow(QMainWindow):

    def DOROBOTTHING(self):
        print("You sent a command")
    # ================================================================
        
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Robot Controller")
        self.setGeometry(50, 50, 640, 480)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for central widget
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.grid_layout = QGridLayout()

        # Navbar with Init and Operate buttons
        self.navbar_layout = QHBoxLayout()
        self.init_button = QPushButton("Init")
        self.init_button.clicked.connect(self.open_init_screen)
        self.init_button.setStyleSheet("QPushButton { background-color:#FF5733; color: black; border:2px solid black; border-radius:30px;padding:15px; min-width :15px;min-height:35px; border-style:outset; border-width:2px; font:bold 14px;}")
        self.operate_button = QPushButton("Operate")
        self.operate_button.setStyleSheet("QPushButton { background-color: #FFC300; color: black;border:2px solid black; border-radius:30px;padding:15px; min-width :15px;min-height:35px; border-style:outset; border-width:2px; font:bold 14px;}")
        self.navbar_layout.addWidget(self.init_button)
        self.navbar_layout.addWidget(self.operate_button)
        self.central_layout.addLayout(self.navbar_layout)

        # Text entry and send button
        self.text_entry_layout = QHBoxLayout()
        self.text_entry = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.text_entry_layout.addWidget(self.text_entry)
        self.text_entry_layout.addWidget(self.send_button)
        self.central_layout.addLayout(self.text_entry_layout)

        # Initialize the boardArray to an 8x8 matrix of zeros
        self.boardArray = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Create an instance of InitScreen and connect signal
        self.init_screen = InitScreen()
        self.init_screen.initComplete.connect(self.update_grid)

        # Display the initial grid
        self.updateGrid()

    def open_init_screen(self):
        self.init_screen.show()

    def update_grid(self, board_array):
        # Update the boardArray with the received data
        self.boardArray = board_array
        # Update the grid display
        self.updateGrid()

    def updateGrid(self):
        # Clear any existing items in grid layout
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        # Display grid of 8x8 buttons based on boardArray
        self.grid_layout = QGridLayout()
        for i in reversed(range(8)):
            for j in range(8):
                button_text = "1" if self.boardArray[i][j] == 1 else "0"
                label_text = str(i*8 + j + 1)
                button_widget = ButtonWithLabel(button_text, label_text)
                self.grid_layout.addWidget(button_widget, 7 - i, j)  # Add button to the reversed row index
        self.central_layout.addLayout(self.grid_layout)

    def send_message(self):
        msg = self.text_entry.text()
        # print(msg)
        newboardArray = algorithm(self.boardArray, msg)
        self.boardArray = newboardArray
        self.updateGrid()

    # ======================= Robot Operations ============================
    def operate_robot(self):
        msg = self.text_entry.text()
        # Call operateRobot function with the message
        self.DOROBOTTHING()


# ===============  END OF MAIN CLASS, BEGIN OF INIT WINDOW CLASS ==========

# Init screen class
class InitScreen(QMainWindow):
     # Define a signal to indicate that initialization is complete
    initComplete = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Init Screen")
        self.setGeometry(200, 200, 400, 300)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for central widget
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        # Central grid display
        self.grid_layout = QGridLayout()
        self.central_layout.addLayout(self.grid_layout)

        # Display grid of 8x8 buttons
        for i in reversed(range(8)):
            for j in range(8):
                button = QPushButton("0")
                button.setStyleSheet("QPushButton { border: 2px solid blue; }")
                button.clicked.connect(lambda _, x=7-i, y=j: self.toggle_button(x, y))
                self.grid_layout.addWidget(button, 7-i, j)  #about placement

    # def init_grid_display(self):
    #     # Clear any existing items in grid layout
    #     for i in reversed(range(self.grid_layout.count())):
    #         widget_to_remove = self.grid_layout.itemAt(i).widget()
    #         if widget_to_remove:
    #             self.grid_layout.removeWidget(widget_to_remove)
    #             widget_to_remove.setParent(None)
        # Display grid of 8x8 buttons
        # for i in reversed(range(8)):
        #     for j in range(8):
        #         button = QPushButton("0")  
        #         button.setFixedSize(40, 40)
        #         button.clicked.connect(lambda _, x=7-i, y=j: self.toggle_button(x, y))
        #         self.grid_layout.addWidget(button, i, j)

    def toggle_button(self, i, j):
        button = self.grid_layout.itemAtPosition(i, j).widget()
        current_text = button.text()
        new_text = "1" if current_text == "0" else "0"
        button.setText(new_text)
        button.setStyleSheet("QPushButton { background-color: green; border: 2px solid red; }" if new_text == "1" else "QPushButton { border: 2px solid blue; }")
        self.boardArray = [[int(self.grid_layout.itemAtPosition(x, y).widget().text()) for y in range(8)] for x in reversed(range(8))]
        self.initComplete.emit(self.boardArray)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())