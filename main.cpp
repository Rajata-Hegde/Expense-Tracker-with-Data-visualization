#include <iostream>
#include <string>
#include <unordered_map>
#include <stack>
#include <queue>
#include <vector>
#include <list>
#include <iomanip>
#include <fstream>
#include <stdexcept>
using namespace std;
struct Expense {
    string category;
    double amount;
    string date;
    Expense* next;  
    Expense(string c, double a, string d, Expense* n = nullptr)
        : category(c), amount(a), date(d), next(n) {}
};
struct TreeNode {
    Expense* expense;
    TreeNode* left;
    TreeNode* right;
    TreeNode(Expense* e) : expense(e), left(nullptr), right(nullptr) {}
};

class ExpenseTracker {
private:
    Expense* expenseHead;  // Linked list for expenses
    unordered_map<string, double> categoryTotals;  // HashMap for totals by category
    stack<Expense*> undoStack;  // Stack to undo actions
    queue<string> recentExpenses;  // Queue for tracking recent categories
    TreeNode* bstRoot;  // Root of the BST
    const int maxRecent = 5; // Max recent categories to track
    const string expenseFile = "expense.csv";  // CSV file to store expenses
    void insertToBST(TreeNode*& root, Expense* expense) {
        if (!root) {
            root = new TreeNode(expense);
            return;
        }
        if (expense->amount < root->expense->amount || 
           (expense->amount == root->expense->amount && expense->category < root->expense->category)) {
            insertToBST(root->left, expense);
        } else {
            insertToBST(root->right, expense);
        }
    }
    void inOrderTraversal(TreeNode* root) {
        if (!root) return;
        inOrderTraversal(root->left);
        cout << "Category: " << root->expense->category 
             << ", Amount: " << fixed << setprecision(2) << root->expense->amount
             << ", Date: " << root->expense->date << endl;
        inOrderTraversal(root->right);
    }
    void rangeQuery(TreeNode* root, double minAmount, double maxAmount) {
        if (!root) return;
        if (root->expense->amount >= minAmount) {
            rangeQuery(root->left, minAmount, maxAmount);
        }
        if (root->expense->amount >= minAmount && root->expense->amount <= maxAmount) {
            cout << "Category: " << root->expense->category << ", Amount: " << fixed << setprecision(2) << root->expense->amount
                 << ", Date: " << root->expense->date << endl;
        }
        if (root->expense->amount <= maxAmount) {
            rangeQuery(root->right, minAmount, maxAmount);
        }
    }

    // Delete BST nodes
    void deleteBST(TreeNode* root) {
        if (!root) return;
        deleteBST(root->left);
        deleteBST(root->right);
        delete root;
    }

    // Save expenses to CSV file
   // Save expenses to CSV file (modified to only write category and amount)
// Save expenses to CSV file with the desired format: category, amount, date
void saveToCSV() {
    ofstream file(expenseFile);
    if (!file.is_open()) {
        cerr << "Error opening file for writing." << endl;
        return;
    }

    // Writing headers to CSV file
    file << "category,amount,date\n";

    // Write each expense entry in the format: category, amount, date
    Expense* temp = expenseHead;
    while (temp) {
        file << temp->category << ","
             << fixed << setprecision(2) << temp->amount << ","
             << temp->date << endl;
        temp = temp->next;
    }
    file.close();
    cout << "Expenses saved to " << expenseFile << endl;
}
public:
    ExpenseTracker() : expenseHead(nullptr), bstRoot(nullptr) {}

    ~ExpenseTracker() {
        deleteBST(bstRoot);
    }

    // Add an expense
    void addExpense() {
        string category, date;
        double amount;

        cout << "Enter category: ";
        cin >> category;
        cout << "Enter amount: ";
        cin >> amount;

        if (amount <= 0) {
            cerr << "Error: Amount must be greater than 0." << endl;
            return;
        }

        cout << "Enter date (YYYY-MM-DD): ";
        cin >> date;

        if (date.length() != 10 || date[4] != '-' || date[7] != '-') {
            cerr << "Error: Invalid date format. Use YYYY-MM-DD." << endl;
            return;
        }

        Expense* newExpense = new Expense(category, amount, date, expenseHead);
        expenseHead = newExpense;
        categoryTotals[category] += amount;

        if (recentExpenses.size() >= maxRecent) {
            recentExpenses.pop();
        }
        recentExpenses.push(category);

        undoStack.push(newExpense);
        insertToBST(bstRoot, newExpense);

        saveToCSV();  // Save updated expenses to CSV

        cout << "Expense added successfully!" << endl;
    }

    void visualizeExpenses() {
        // Command to run the Python script
        string command = "python visualization.py expense.csv";  // Make sure the correct file path is passed
        
        // Execute the Python script to visualize the expenses
        int result = system(command.c_str());

        if (result != 0) {
            cout << "Error running the visualization script!" << endl;
        } else {
            cout << "Expenses visualization complete!" << endl;
        }
    }

    // View all expenses
    void viewAllExpenses() {
        Expense* temp = expenseHead;
        if (!temp) {
            cout << "No expenses available." << endl;
            return;
        }

        cout << "All Expenses:" << endl;
        while (temp != nullptr) {
            cout << "Category: " << temp->category << ", Amount: " << fixed << setprecision(2) << temp->amount
                 << ", Date: " << temp->date << endl;
            temp = temp->next;
        }
    }

    // View expenses by category
    void viewExpensesByCategory() {
        string category;
        cout << "Enter category: ";
        cin >> category;

        Expense* temp = expenseHead;
        bool found = false;

        cout << "Expenses in category '" << category << "':" << endl;
        while (temp != nullptr) {
            if (temp->category == category) {
                cout << "Amount: " << fixed << setprecision(2) << temp->amount
                     << ", Date: " << temp->date << endl;
                found = true;
            }
            temp = temp->next;
        }

        if (!found) {
            cout << "No expenses found in this category." << endl;
        }
    }

    // View total amount by category
    void viewCategoryTotals() {
        if (categoryTotals.empty()) {
            cout << "No expenses available." << endl;
            return;
        }

        cout << "Category Totals:" << endl;
        for (const auto& pair : categoryTotals) {
            cout << "Category: " << pair.first << ", Total: " << fixed << setprecision(2) << pair.second << endl;
        }
    }

    // View recent categories
    void viewRecentCategories() {
        if (recentExpenses.empty()) {
            cout << "No recent expenses recorded." << endl;
            return;
        }

        cout << "Recent Expense Categories:" << endl;
        queue<string> tempQueue = recentExpenses;
        while (!tempQueue.empty()) {
            cout << tempQueue.front() << endl;
            tempQueue.pop();
        }
    }

    // Undo the last added expense
    void undoLastExpense() {
        if (undoStack.empty()) {
            cout << "No actions to undo." << endl;
            return;
        }

        Expense* lastExpense = undoStack.top();
        undoStack.pop();

        categoryTotals[lastExpense->category] -= lastExpense->amount;
        Expense* temp = expenseHead;

        if (expenseHead == lastExpense) {
            expenseHead = expenseHead->next;
        } else {
            while (temp->next != lastExpense) {
                temp = temp->next;
            }
            temp->next = lastExpense->next;
        }

        delete lastExpense;

        saveToCSV();  // Save updated expenses to CSV

        cout << "Last expense undone." << endl;
    }

    // View expenses sorted by amount
    void viewExpensesSorted() {
        if (!bstRoot) {
            cout << "No expenses available." << endl;
            return;
        }

        cout << "Expenses Sorted by Amount:" << endl;
        inOrderTraversal(bstRoot);
    }

    // View expenses in a range
    void viewExpensesInRange(double minAmount, double maxAmount) {
        if (!bstRoot) {
            cout << "No expenses available." << endl;
            return;
        }

        cout << "Expenses in Range (" << minAmount << " to " << maxAmount << "):" << endl;
        rangeQuery(bstRoot, minAmount, maxAmount);
    }
};
int main() {
    ExpenseTracker tracker;
    int choice;
    while (true) {
        cout << "\nExpense Tracker Menu:" << endl;
        cout << "1. Add Expense" << endl;
        cout << "2. View All Expenses" << endl;
        cout << "3. View Category Totals" << endl;
        cout << "4. View Recent Categories" << endl;
        cout << "5. Undo Last Expense" << endl;
        cout << "6. View Expenses Sorted by Amount" << endl;
        cout << "7. View Expenses in Range" << endl;
        cout << "8. View Expenses by Category" << endl;
        cout << "9. Visualize Expenses" << endl;
        cout << "10. Exit" << endl;
        cout << "Enter your choice: ";
        cin >> choice;
        switch (choice) {
            case 1: tracker.addExpense(); break;
            case 2: tracker.viewAllExpenses(); break;
            case 3: tracker.viewCategoryTotals(); break;
            case 4: tracker.viewRecentCategories(); break;
            case 5: tracker.undoLastExpense(); break;
            case 6: tracker.viewExpensesSorted(); break;
            case 7: {
                double minAmount, maxAmount;
                cout << "Enter minimum amount: ";
                cin >> minAmount;
                cout << "Enter maximum amount: ";
                cin >> maxAmount;
                tracker.viewExpensesInRange(minAmount, maxAmount);
                break;
            }
            case 8: tracker.viewExpensesByCategory(); break;
            case 9: tracker.visualizeExpenses(); break;  // Call the visualization option
            case 10: return 0;
            default: cout << "Invalid choice!" << endl;
        }
    }
}
