import sys
from PyQt6.QtWidgets import QApplication
from reminder_choice_ui import ReminderChoiceWindow

class FlowerCareApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = ReminderChoiceWindow(self)
        
    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    flower_app = FlowerCareApp()
    flower_app.run()