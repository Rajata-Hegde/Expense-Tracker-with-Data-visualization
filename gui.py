import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel,
    QFileDialog, QTableWidget, QTableWidgetItem, QStackedWidget, QComboBox, QCalendarWidget,
    QWidget, QAction, QHBoxLayout, QMessageBox, QRadioButton, QButtonGroup, QHeaderView, 
    QDialogButtonBox, QDialog
)
from PyQt5.QtCore import Qt
from fpdf import FPDF
from PyQt5.QtGui import QPixmap
from datetime import datetime
import matplotlib.pyplot as plt  # For generating charts in the report (Optional)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
class ExpenseTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 200, 800, 600)

        self.expenses = []
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        self.page1 = self.create_home_page()
        self.page2 = self.create_add_expense_page()
        self.page3 = self.create_view_expenses_page()
        self.page4 = self.create_summary_page()
        self.page5 = self.create_dashboard_page()
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)
        self.stack.addWidget(self.page4)
        self.stack.addWidget(self.page5)
    def create_home_page(self):
        home_page = QWidget(self)
        layout = QVBoxLayout(home_page)
        add_expense_button = self.create_styled_button("Add Expense", "#4CAF50")
        view_expenses_button = self.create_styled_button("View Expenses", "#2196F3")
        summary_button = self.create_styled_button("View Summary", "#FFC107")
        dashboard_button = self.create_styled_button("Dashboard", "#FF5722")
        image_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\rajat\\OneDrive\\Desktop\\Expense_Tracker\\.vscode\\expense.png")  # Replace with an actual image file path
        if pixmap.isNull():
            print("Error: Image not found!")
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)
        welcome_text = QLabel("<b>Welcome to your Expense Tracker!", self)
        welcome_text.setStyleSheet("font-size: 24px; color:rgb(96, 76, 175); text-align: center;")
        layout.addWidget(welcome_text)
        layout.addWidget(add_expense_button)
        layout.addWidget(view_expenses_button)
        layout.addWidget(summary_button)
        layout.addWidget(dashboard_button)
        add_expense_button.clicked.connect(self.go_to_add_expense_page)
        view_expenses_button.clicked.connect(self.go_to_view_expenses_page)
        summary_button.clicked.connect(self.go_to_summary_page)
        dashboard_button.clicked.connect(self.go_to_dashboard_page)
        return home_page
    def create_add_expense_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Food", "Transportation", "Utilities", "Entertainment", "Other", "Health", "Education"])
        self.category_input.setStyleSheet("""
            QComboBox {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                background-color: #f0f0f0;
            }
            QComboBox:hover ```python
            {
                border-color: #2196F3;
                background-color: #ffffff;
            }
            QComboBox:focus {
                border-color: #2196F3;
                background-color: #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                font-size: 16px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                background-color: #f0f0f0;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: #ffffff;
            }
        """)
        self.date_input = QCalendarWidget(self)
        self.category_input.currentTextChanged.connect(self.enable_custom_category_input)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_input)
        self.custom_category_input = QLineEdit(self)
        self.custom_category_input.setPlaceholderText("Enter custom category")
        self.custom_category_input.setEnabled(False)
        layout.addWidget(self.custom_category_input)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_input)
        submit_button = self.create_styled_button("Submit", "#8BC34A")
        layout.addWidget(submit_button)
        submit_button.clicked.connect(self.submit_expense)
        back_button = self.create_styled_button("Go Back", "#ff5722")
        layout.addWidget(back_button)
        back_button.clicked.connect(self.go_back)
        return page
    def enable_custom_category_input(self, text):
        if text == "Other":
            self.custom_category_input.setEnabled(True)
            self.custom_category_input.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 16px;
                    background-color: #f0f0f0;
                }
                QLineEdit:focus {
                    border-color: #2196F3;
                    background-color: #ffffff;
                }
            """)
        else:
            self.custom_category_input.setEnabled(False)
    def create_view_expenses_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        search_layout = QHBoxLayout()
        search_label = QLabel("Search by Category:", self)
        self.search_input = QLineEdit(self)
        search_button = self.create_styled_button("Search", "#8BC34A")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)
        sort_layout = QHBoxLayout()
        sort_label = QLabel("Sort by:", self)
        self.sort_combo = QComboBox(self)
        self.sort_combo.addItems(["Highest Expense", "Least Expense", "Newest First", "Oldest First"])
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        layout.addLayout(sort_layout)
        self.expenses_table = QTableWidget(self)
        self.expenses_table.setColumnCount(3)
        self.expenses_table.setHorizontalHeaderLabels(["Category", "Amount", "Date"])
        self.expenses_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make the table non-editable directly
        self.expenses_table.setSelectionBehavior(QTableWidget.SelectRows)  # Select full rows
        layout.addWidget(self.expenses_table)
        self.edit_button = self.create_styled_button("Edit Expense", "#FF9900")
        self.delete_button = self.create_styled_button("Delete Expense", "#F44336")
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        search_button.clicked.connect(self.search_expenses)
        self.sort_combo.currentTextChanged.connect(lambda: self.update_expenses_table())
        self.edit_button.clicked.connect(self.edit_expense)
        self.delete_button.clicked.connect(self.delete_expense)
        back_button = self.create_styled_button("Go Back", "#ff5722")
        layout.addWidget(back_button)
        back_button.clicked.connect(self.go_back)
        return page
    def search_expenses(self):
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.update_expenses_table(self.expenses)
        else:
            filtered_expenses = [
                expense for expense in self.expenses if search_term in expense['category'].lower()
            ]
            self.update_expenses_table(filtered_expenses)
    def update_expenses_table(self, expenses=None):
        if expenses is None:
            expenses = self.expenses  
        if not isinstance(expenses, list):
            print("Error: expenses is not a list!")
            return
        sort_option = self.sort_combo.currentText()
        if sort_option == "Highest Expense":
            expenses.sort(key=lambda x: x["amount"], reverse=True)
        elif sort_option == "Least Expense":
            expenses.sort(key=lambda x: x["amount"])
        elif sort_option == "Newest First":
            expenses.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
        elif sort_option == "Oldest First":
            expenses.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
        self.expenses_table.setRowCount(0)
        for expense in expenses:
            row_position = self.expenses_table.rowCount()
            self.expenses_table.insertRow(row_position)
            self.expenses_table.setItem(row_position, 0, QTableWidgetItem(expense['category']))
            self.expenses_table.setItem(row_position, 1, QTableWidgetItem(f"${expense['amount']:.2f}"))
            self.expenses_table.setItem(row_position, 2, QTableWidgetItem(expense['date']))
    def edit_expense(self):
        selected_row = self.expenses_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an expense to edit.")
            return
        selected_expense = self.expenses[selected_row]
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Expense")
        form_layout = QFormLayout(dialog)
        category_input = QLineEdit(selected_expense['category'])
        amount_input = QLineEdit(str(selected_expense['amount']))
        date_input = QLineEdit(selected_expense['date'])
        form_layout.addRow("Category:", category_input)
        form_layout.addRow("Amount:", amount_input)
        form_layout.addRow("Date:", date_input)
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        form_layout.addWidget(button_box)
        button_box.accepted.connect(lambda: self.save_edit_expense(selected_row, category_input, amount_input, date_input, dialog))
        button_box.rejected.connect(dialog.reject)
        dialog.exec_()
    def save_edit_expense(self, row, category_input, amount_input, date_input, dialog):
        updated_expense = {
            "category": category_input.text(),
            "amount": float(amount_input.text()),
            "date": date_input.text()
        }
        self.expenses[row] = updated_expense
        self.update_expenses_table(self.expenses)
        dialog.accept()
    def delete_expense(self):
        selected_row = self.expenses_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an expense to delete.")
            return
        reply = QMessageBox.question(self, "Delete Expense", "Are you sure you want to delete this expense?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.expenses[selected_row]
            self.update_expenses_table(self.expenses)
    def create_styled_button(self, text, color):
        button = QPushButton(text, self)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color_brightness(color, -20)};
            }}
        """)
        return button
    def create_summary_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        title_label = QLabel("Expense Report :Generate report for your expenses and save it", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignBottom)
        layout.addWidget(title_label)
        name_layout = QHBoxLayout()
        name_label = QLabel("Enter Your Name:", self)
        name_label.setStyleSheet("font-size: 16px;")
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Your name here")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: #f0f0f0;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: #ffffff;
            }
        """)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        filter_layout = QHBoxLayout()
        self.year_filter = QComboBox(self)
        self.year_filter.addItem("Select Year")
        for year in range(2020, 2026):
            self.year_filter.addItem(str(year))
        self.month_filter = QComboBox(self)
        self.month_filter.addItem("Select Month")
        month_names = [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ]
        
        for month in month_names:
            self.month_filter.addItem(month)
        filter_layout.addWidget(QLabel("Year:"))
        filter_layout.addWidget(self.year_filter)
        filter_layout.addWidget(QLabel("Month:"))
        filter_layout.addWidget(self.month_filter)
        layout.addLayout(filter_layout)
        category_layout = QHBoxLayout()
        self.category_filter = QComboBox(self)
        self.category_filter.addItem("All")
        self.category_filter.addItems([
            "Food", "Transportation", "Utilities", "Entertainment", 
            "Other", "Health", "Education"
        ])
        category_layout.addWidget(QLabel("Category:"))
        category_layout.addWidget(self.category_filter)
        layout.addLayout(category_layout)
        generate_report_button = self.create_styled_button("Generate Report (PDF)", "#4CAF50")
        layout.addWidget(generate_report_button)
        generate_report_button.clicked.connect(self.generate_pdf_report)
        back_button = self.create_styled_button("Go Back", "#ff5722")
        layout.addWidget(back_button)
        back_button.clicked.connect(self.go_back)
        return page
    def generate_pdf_report(self):
        user_name = self.name_input.text().strip()
        if not user_name:
            QMessageBox.warning(self, "Input Error", "Please enter your name to generate the report.")
            return
        selected_year = self.year_filter.currentText()
        selected_month = self.month_filter.currentText()
        selected_category = self.category_filter.currentText()
        if selected_year == "Select Year":
            selected_year = None
        if selected_month == "Select Month":
            selected_month = None
        filtered_expenses = [
            expense for expense in self.expenses if 
            (selected_year is None or expense['date'].startswith(selected_year)) and
            (selected_month is None or expense['date'][5:7] == f"{month_names.index(selected_month)+1:02}") and
            (selected_category == "All" or expense['category'] == selected_category)
        ]
        
        if not filtered_expenses:
            QMessageBox.warning(self, "No Data", "No expenses match your filters.")
            return
        total_expenses = sum(expense['amount'] for expense in filtered_expenses)
        expenses_by_category = {}
        for expense in filtered_expenses:
            category = expense['category']
            expenses_by_category[category] = expenses_by_category.get(category, 0) + expense['amount']
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Expense Report", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Generated by: {user_name}", ln=True, align="L")
        if selected_year:
            pdf.cell(200, 10, txt=f"Year: {selected_year}", ln=True, align="L")
        if selected_month:
            pdf.cell(200, 10, txt=f"Month: {selected_month}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Category: {selected_category}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Total Expenses: ${total_expenses:.2f}", ln=True, align="L")
        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="Total Expenses by Category:", ln=True, align="L")
        pdf.set_font("Arial", size=12)
        for category, total in expenses_by_category.items():
            pdf.cell(200, 10, txt=f"{category}: ${total:.2f}", ln=True, align="L")
        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(60, 10, txt="Category", border=1, align="C")
        pdf.cell(40, 10, txt="Amount", border=1, align="C")
        pdf.cell(40, 10, txt="Date", border=1, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        for expense in filtered_expenses:
            pdf.cell(60, 10, txt=expense['category'], border=1, align="L")
            pdf.cell(40, 10, txt=f"${expense['amount']:.2f}", border=1, align="R")
            pdf.cell(40, 10, txt=expense['date'], border=1, align="C")
            pdf.ln(10)
        
        # Save the PDF file
        file_path = QFileDialog.getSaveFileName(self, "Save Report", f"{user_name}_Expense_Report.pdf", "PDF Files (*.pdf)")[0]
        if file_path:
            pdf.output(file_path)
            QMessageBox.information(self, "Success", f"Report saved successfully as {file_path}!")
        else:
            QMessageBox.warning(self, "Save Cancelled", "Report generation was cancelled.")

    def create_dashboard_page(self):
        page = QWidget(self)
        layout = QVBoxLayout(page)
        chart_type_label = QLabel("Select Chart Type:", self)
        chart_type_label.setStyleSheet("font-size: 16px; color: #333;")
        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems(["Bar Chart", "Pie Chart", "Line Chart"])
        self.chart_type_combo.setStyleSheet("font-size: 14px; padding: 4px;")
        layout.addWidget(chart_type_label)
        layout.addWidget(self.chart_type_combo)
        canvas = FigureCanvas(plt.figure(figsize=(7, 5)))
        layout.addWidget(canvas)
        self.plot_expenses_by_category(canvas)
        self.chart_type_combo.currentTextChanged.connect(lambda: self.update_plot(canvas))
        back_button = self.create_styled_button("Go Back", "#ff5722")
        layout.addWidget(back_button)
        back_button.clicked.connect(self.go_back)
        return page
    def plot_expenses_by_category(self, canvas):
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense["category"]] = category_totals.get(expense["category"], 0) + expense["amount"]
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        self.update_plot(canvas, categories, amounts)
    def update_plot(self, canvas, categories=None, amounts=None):
        if categories is None or amounts is None:
            category_totals = {}
            for expense in self.expenses:
                category_totals[expense["category"]] = category_totals.get(expense["category"], 0) + expense["amount"]
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
        plt.clf()  
        chart_type = self.chart_type_combo.currentText()
        ax = canvas.figure.add_subplot(111)
        ax.set_facecolor("#f5f5f5")
        ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7)
        if chart_type == "Bar Chart":
            ax.bar(categories, amounts, color='skyblue', edgecolor='black')
            ax.set_title("Expenses by Category", fontsize=16, color="#333")
            ax.set_xlabel("Category", fontsize=14, color="#333")
            ax.set_ylabel("Amount", fontsize=14, color="#333")
            ax.tick_params(axis='x', labelrotation=45, labelsize=12)
            ax.tick_params(axis='y', labelsize=12)
        elif chart_type == "Pie Chart":
            ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            ax.set_title("Expenses by Category", fontsize=16, color="#333")
        elif chart_type == "Line Chart":
            ax.plot(categories, amounts, marker='o', linestyle='-', color='b')
            ax.set_title("Expenses by Category (Line Chart)", fontsize=16, color="#333")
            ax.set_xlabel("Category", fontsize=14, color="#333")
            ax.set_ylabel("Amount", fontsize=14, color="#333")
            ax.tick_params(axis='x', labelrotation=45, labelsize=12)
            ax.tick_params(axis='y', labelsize=12)
        canvas.figure.tight_layout()  
        canvas.draw()
    def create_styled_button(self, text, color):
        button = QPushButton(text)
        button.setStyleSheet(f"background-color: {color}; color: white; font-size: 18px; padding: 10px; border-radius: 5px;")
        return button
    def go_back(self):
        self.stack.setCurrentIndex(0)  
    def go_to_add_expense_page(self):
        self.stack.setCurrentIndex(1)
    def go_to_view_expenses_page(self):
        self.stack.setCurrentIndex(2)
    def go_to_summary_page(self):
        self.stack.setCurrentIndex(3)
    def go_to_dashboard_page(self):
        self.stack.setCurrentIndex(4)
    def submit_expense(self):
        category = self.category_input.currentText()
        if category == "Other":
            category = self.custom_category_input.text().strip()
        if not category:
            QMessageBox.warning(self, "Input Error", "Please enter a valid category.")
            return
        try:
            amount = float(self.amount_input.text().strip())
            date = self.date_input.selectedDate().toString("yyyy-MM-dd")
            self.expenses.append({"category": category, "amount": amount, "date": date})
            self.update_expenses_table()
            self.category_input.setCurrentIndex(0)  
            self.custom_category_input.clear() 
            self.custom_category_input.setEnabled(False) 
            self.amount_input.clear()  
            self.date_input.setSelectedDate(self.date_input.selectedDate()) 
            QMessageBox.information(self, "Success", "Your expense has been added successfully!")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTrackerApp()
    window.show()
    sys.exit(app.exec_())
