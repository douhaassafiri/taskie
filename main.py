from PySide6.QtWidgets import QApplication, QTabWidget, QWidget, QFormLayout, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QComboBox
import sys

PRIORITY_EMOJIS = {
    "🌱 Low": "🌱",
    "⭐ Medium": "⭐",
    "🔥 High": "🔥"
}

CATEGORY_EMOJIS = {
    "📋 General": "📋",
    "💼 Work": "💼",
    "🧸 Personal": "🧸",
    "📚 Study": "📚",
    "🛍️ Shopping": "🛍️"
}

def load_stylesheet(path):
    with open(path, 'r') as file:
        return file.read()

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taskie 🎀")
        self.setFixedSize(400, 500)

        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # --- Tasks tab ---
        self.tasks_tab = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_tab)

        self.filter_category = QComboBox()
        self.filter_category.addItems([
            "📂 Show All Categories", "📋 General", "💼 Work", "🧸 Personal", "📚 Study", "🛍️ Shopping"
        ])
        self.filter_category.currentTextChanged.connect(self.filter_tasks)
        self.tasks_layout.addWidget(self.filter_category)

        self.filter_priority = QComboBox()
        self.filter_priority.addItems([
            "📊 Show All Priorities", "🌱 Low", "⭐ Medium", "🔥 High"
        ])
        self.filter_priority.currentTextChanged.connect(self.filter_tasks)
        self.tasks_layout.addWidget(self.filter_priority)

        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.delete_task)
        self.tasks_layout.addWidget(self.task_list)

        self.tabs.addTab(self.tasks_tab, "Tasks")

        # --- Add Task tab ---
        self.add_tab = QWidget()
        self.add_layout = QVBoxLayout(self.add_tab)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Add a new task...")
        self.add_layout.addWidget(self.task_input)

        self.category_select = QComboBox()
        self.category_select.addItem("Select Category")
        self.category_select.setCurrentIndex(0)
        self.category_select.addItems([
            "📋 General", "💼 Work", "🧸 Personal", "📚 Study", "🛍️ Shopping"
        ])
        self.add_layout.addWidget(self.category_select)

        self.priority_select = QComboBox()
        self.priority_select.addItem("Select Priority")
        self.priority_select.setCurrentIndex(0)
        self.priority_select.addItems([
            "🌱 Low", "⭐ Medium", "🔥 High"
        ])
        self.add_layout.addWidget(self.priority_select)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        self.add_layout.addWidget(self.add_button)

        self.tabs.addTab(self.add_tab, "Add Task")

        self.all_tasks = []
        self.load_tasks()

    def add_task(self):
        text = self.task_input.text()
        category = self.category_select.currentText()
        priority = self.priority_select.currentText()

        if text and category != "Select Category" and priority != "Select Priority":
            self.all_tasks.append((category, text, priority))
            self.update_task_list()
            self.task_input.clear()

            self.category_select.setCurrentIndex(0)
            self.priority_select.setCurrentIndex(0)

            self.save_tasks()

    def delete_task(self, item):
        index = self.task_list.row(item)
        self.task_list.takeItem(index)
        if 0 <= index < len(self.all_tasks):
            del self.all_tasks[index]
        self.save_tasks()

    def update_task_list(self):
        self.task_list.clear()
        selected_category = self.filter_category.currentText()
        selected_priority = self.filter_priority.currentText()

        for category, text, priority in self.all_tasks:
            category_match = (selected_category == "📂 Show All Categories" or category == selected_category)
            priority_match = (selected_priority == "📊 Show All Priorities" or priority == selected_priority)

            if category_match and priority_match:
                priority_emoji = PRIORITY_EMOJIS.get(priority, "")
                category_emoji = CATEGORY_EMOJIS.get(category, "")
                self.task_list.addItem(f"{priority_emoji} {category_emoji} {text}")

    def filter_tasks(self, selected_filter):
        self.update_task_list()

    def save_tasks(self):
        with open("tasks.txt", "w", encoding="utf-8") as file:
            for category, text, priority in self.all_tasks:
                file.write(f"{category}|{text}|{priority}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        category, text, priority = parts
                        self.all_tasks.append((category, text, priority))
            self.update_task_list()
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("style.qss"))
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())