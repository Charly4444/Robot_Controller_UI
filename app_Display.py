import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QGridLayout
from PyQt5.QtCore import QObject, pyqtSignal
from algo import algorithmManager as algorithm

class MainWindow(QMainWindow):
    def DOROBOTTHING(self):
        print("You sent a command")
    
    # ================================================================
        
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Robot Controller")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for central widget
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        # Navbar
        self.navbar_layout = QHBoxLayout()
        self.init_button = QPushButton("Init")
        self.init_button.clicked.connect(self.open_init_screen)
        self.operate_button = QPushButton("Operate")
        self.operate_button.clicked.connect(self.operate_robot)
        self.navbar_layout.addWidget(self.init_button)
        self.navbar_layout.addWidget(self.operate_button)
        self.central_layout.addLayout(self.navbar_layout)

        # Central grid display
        self.grid_layout = QGridLayout()
        self.central_layout.addLayout(self.grid_layout)

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
        
        # Display the initial grid
        self.updateGrid()


    def initializeBoardArray(self):
        # Reset the boardArray to an 8x8 matrix of zeros
        self.boardArray = [[0] * 8 for _ in range(8)]
        self.updateGrid()

    def updateGrid(self):
        # Clear any existing items in grid layout
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        # Display grid of 8x8 buttons based on boardArray
        for i in range(8):
            for j in range(8):
                value = self.boardArray[i][j]
                button_text = "x" if value == 1 else "o"
                button = QPushButton(button_text)
                self.grid_layout.addWidget(button, i, j)
        
        # Create an instance of InitScreen
        self.init_screen = InitScreen()

        # Connect the initComplete signal to updateGrid slot
        self.init_screen.initComplete.connect(self.update_grid)

    def open_init_screen(self):
        # Show the init screen
        self.init_screen.show()

    def update_grid(self, board_array):
        # Update the boardArray with the received data
        self.boardArray = board_array

        # Update the grid display
        self.updateGrid()
    # ======================= Robot Operations ============================
    def operate_robot(self):
        msg = self.text_entry.text()
        # Call operateRobot function with the message
        self.DOROBOTTHING()

    # send message so it will be processed
    def send_message(self):
        msg = self.text_entry.text()
        newboardArray = algorithm(self.boardArray,msg)
        self.boardArray = newboardArray
        self.update_grid(self.boardArray)
    # =====================================================================
    
    def init_grid_display(self):
        # Clear any existing items in grid layout
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        # Display grid of 8x8 buttons
        for i in range(8):
            for j in range(8):
                button = QPushButton("0")
                button.clicked.connect(self.toggle_button)  # Connect button click signal to toggle_button
                self.grid_layout.addWidget(button, i, j)

    def toggle_button(self):
        # Toggle the value of the clicked button (0 -> 1, 1 -> 0)
        sender_button = self.sender()
        if sender_button.text() == "0":
            sender_button.setText("1")
        else:
            sender_button.setText("0")

# ===============  END OF MAIN CLASS, BEGIN OF INIT WINDOW CLASS ==========

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

        # Navbar
        self.navbar_layout = QHBoxLayout()
        self.init_button = QPushButton("Init")
        self.init_button.setEnabled(False)  # Disable init button on init screen
        self.operate_button = QPushButton("Operate")
        self.operate_button.clicked.connect(self.close)  # Close init screen on operate button click
        self.navbar_layout.addWidget(self.init_button)
        self.navbar_layout.addWidget(self.operate_button)
        self.central_layout.addLayout(self.navbar_layout)

        # Central grid display
        self.grid_layout = QGridLayout()
        self.central_layout.addLayout(self.grid_layout)
        
        # Initialize button
        self.initialize_button = QPushButton("Initialize")
        self.initialize_button.clicked.connect(self.set_board_array)
        self.central_layout.addWidget(self.initialize_button)

        # Clear any existing items in grid layout and show blanks button
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        # Display grid of 8x8 buttons
        for i in range(8):
            for j in range(8):
                button = QPushButton("0")
                button.clicked.connect(self.toggle_button)  # Connect button click signal to toggle_button
                self.grid_layout.addWidget(button, i, j)


    def toggle_button(self):
        # Toggle the value of the clicked button (0 -> 1, 1 -> 0)
        sender_button = self.sender()
        if sender_button.text() == "0":
            sender_button.setText("1")
        else:
            sender_button.setText("0")

    def set_board_array(self):
        # Initialize the boardArray based on button values
        self.boardArray = [[int(self.grid_layout.itemAtPosition(i, j).widget().text()) for j in range(8)] for i in range(8)]
        self.close()  # Close the init screen

        # Emit the initComplete signal with the updated boardArray
        self.initComplete.emit(self.boardArray)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
