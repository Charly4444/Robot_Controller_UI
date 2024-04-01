from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal, QTimer
# Supposons que "algo" est le module contenant "algorithmManager"
from algo import algorithmManager as algorithm
from generateautomoves import generate_moves
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

    # ================================================================
        
    def __init__(self):
        super().__init__()

        

        # using QTimer to synchronize
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.apply_next_move)
        self.moves_list = []

        
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
        self.operate_button.clicked.connect(self.open_auto_screen)
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

        self.wanted_array = [
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

        # Create the Sort button
        self.sort_button = QPushButton("Sort")
        self.sort_button.clicked.connect(self.auto_arrange)

        # create an instance of Autoscreen and pass in sort button widget to make it show
        self.auto_screen = AutoScreen(self.sort_button)
        # the value or 'wanted_array' emitted by the init after clicking can be directly used to call the update-wanted method, this is cool
        self.auto_screen.autosComplete.connect(self.update_wanted)

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
        

    def open_auto_screen(self):
        self.auto_screen.show()
    
    # == == == == ==
    def implement_automoves(self, moves_list):
        self.moves_list = moves_list
        self.timer.start(1000)  # Start timer with a 1-second interval

    def apply_next_move(self):
        if self.moves_list:
            move = self.moves_list.pop(0)
            msg = f'Move,{move[0]},{move[1]}'
            newboardArray = algorithm(self.boardArray, msg)
            self.boardArray = newboardArray
            self.updateGrid()
        else:
            self.timer.stop()


        # =====================
    def update_wanted(self, wanted_array):
        # update the wanted array now
        self.wanted_array = wanted_array

    def auto_arrange(self):
        # print(wanted_array)
        
        # get automatic move list
        moves_list = generate_moves(arr1=self.boardArray, arr2=self.wanted_array)

        # implement moves automatika
        self.implement_automoves(moves_list)

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


    def toggle_button(self, i, j):
        button = self.grid_layout.itemAtPosition(i, j).widget()
        current_text = button.text()
        new_text = "1" if current_text == "0" else "0"
        button.setText(new_text)
        button.setStyleSheet("QPushButton { background-color: green; border: 2px solid red; }" if new_text == "1" else "QPushButton { border: 2px solid blue; }")
        self.boardArray = [[int(self.grid_layout.itemAtPosition(x, y).widget().text()) for y in range(8)] for x in reversed(range(8))]
        self.initComplete.emit(self.boardArray)



# ======================= Other Robot Operations ============================

class AutoScreen(QMainWindow):
     # Define a signal to indicate that initialization is complete
    autosComplete = pyqtSignal(list)

    def __init__(self, sort_button):
        super().__init__()

        self.setWindowTitle("Auto Screen")
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

        # Display grid of 8x8 buttons based on boardArray
        for i in reversed(range(8)):
            for j in range(8):
                button_text = "0"
                label_text = str(i*8 + j + 1)
                button_widget = ButtonWithLabel(button_text, label_text)
                button_widget.button.clicked.connect(lambda _, x=7-i, y=j: self.toggle_mybutton(x, y))
                self.grid_layout.addWidget(button_widget, 7 - i, j)  # Add button to the reversed row index

        # Add the sort_button we recieved from main to the layout
        self.central_layout.addWidget(sort_button)

    def toggle_mybutton(self, i, j):
        button_widget = self.grid_layout.itemAtPosition(i, j).widget()
        current_text = button_widget.button.text()
        new_text = "1" if current_text == "0" else "0"
        button_widget.button.setText(new_text)
        button_widget.button.setStyleSheet("QPushButton { background-color: green; border: 2px solid red; }" if new_text == "1" else "QPushButton { border: 2px solid blue; }")
        self.wanted_array = [[int(self.grid_layout.itemAtPosition(x, y).widget().button.text()) for y in range(8)] for x in reversed(range(8))]
        self.autosComplete.emit(self.wanted_array)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

