import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QMouseEvent,QPen, QPainter
from PyQt5.QtCore import Qt 

class MousePositionMemento:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MouseCapture:
    def __init__(self):
        self.positions = []
        self.position_index = -1
    
    def add_position(self, x, y):
        self.positions = self.positions[:self.position_index + 1]
        self.positions.append(MousePositionMemento(x, y))
        self.position_index = len(self.positions) - 1
    
    def undo(self):
        if self.position_index > 0:
            self.position_index -= 1
            return self.positions[self.position_index]
        return None
    
    def redo(self):
        if self.position_index < len(self.positions) - 1:
            self.position_index += 1
            return self.positions[self.position_index]
        return None

class MouseCaptureApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mouse_capture = MouseCapture()

        self.label = QLabel("Eventos", self)
        self.undo_button = QPushButton("Undo", self)
        self.redo_button = QPushButton("Redo", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.undo_button)
        layout.addWidget(self.redo_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.undo_button.clicked.connect(self.undo)
        self.redo_button.clicked.connect(self.redo)

    def mousePressEvent(self, event: QMouseEvent):
        x, y = event.x(), event.y()
        self.mouse_capture.add_position(x, y)
        self.update_label()
        self.draw(x,y)
    def draw(self,x,y):
        qp = QPainter(self)
        qp.setPen(Qt.red)
        qp.begin(self)
        qp.drawPoint(x, y)
        qp.end()
    
        
        
    def undo(self):
        position = self.mouse_capture.undo()
        if position:
            self.label.setText(f"Undo: Mouse Clickeado en ({position.x}, {position.y})")

    def redo(self):
        position = self.mouse_capture.redo()
        if position:
            self.label.setText(f"Redo: Mouse Clickeado en ({position.x}, {position.y})")

    def update_label(self):
        current_position = self.mouse_capture.positions[self.mouse_capture.position_index]
        self.label.setText(f"Mouse Clickeado en ({current_position.x}, {current_position.y})")

def main():
    app = QApplication(sys.argv)
    capture_app = MouseCaptureApp()
    capture_app.setWindowTitle("Capturador de Clicks Con Memento")
    capture_app.setGeometry(100, 100, 800, 600)
    capture_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()