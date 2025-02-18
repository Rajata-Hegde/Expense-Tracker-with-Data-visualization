import matplotlib.pyplot as plt
import csv
from collections import defaultdict

def visualize_expenses(file):
    categories = []
    totals = []

    # Read the expense data
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if row:  # Check if the row is not empty
                try:
                    category = row[0]
                    total = float(row[1])
                    categories.append(category)
                    totals.append(total)
                except ValueError:
                    print(f"Skipping invalid data: {row}")  # Handle invalid data

    # Create a bar chart for total expenditure per category
    category_summary = defaultdict(float)
    for i, category in enumerate(categories):
        category_summary[category] += totals[i]

    # Sort categories by spending amount for better visual hierarchy
    sorted_categories = sorted(category_summary.items(), key=lambda x: x[1], reverse=True)
    sorted_categories, sorted_totals = zip(*sorted_categories)

    # Plot the bar chart with enhanced visual design
    plt.figure(figsize=(10, 6))  # Adjust the figure size for a smaller chart
    bars = plt.bar(sorted_categories, sorted_totals, color=plt.cm.Paired.colors, width=0.4, edgecolor='black', linewidth=1)  # Thinner bars with reduced width

    # Add labels for each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.02, f"${yval:.2f}", ha='center', va='bottom', fontsize=10)

    # Add additional visual elements
    plt.xlabel('Categories', fontsize=12)
    plt.ylabel('Total Spending ($)', fontsize=12)
    plt.title('Total Spending per Category', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Add gridlines for better readability
    plt.tight_layout()  # Ensure everything fits in the figure

    # Show the plot (Bar Chart)
    plt.show()

    # Plot the pie chart
    plt.figure(figsize=(6, 6))  # Smaller figure size for the pie chart
    plt.pie(sorted_totals, labels=sorted_categories, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=140)
    plt.title('Expense Distribution by Category', fontsize=14)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Show the plot (Pie Chart)
    plt.show()

if __name__ == "__main__":
    visualize_expenses("expense.csv")
