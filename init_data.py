import pandas as pd
from datetime import datetime, timedelta

# Create data directory if it doesn't exist
import os
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize goals
goals_data = {
    'goal': ['Summer Savings', 'Trip', 'Gifts', 'Monthly Dates'],
    'target_amount': [3000, 2000, 1000, 2400],  # 200 * 12 months
    'current_amount': [0, 0, 0, 0],
    'deadline': ['2024-08-22', '2024-08-22', '2024-08-22', '2024-05-23']  # Using your end date
}
pd.DataFrame(goals_data).to_csv('data/goals.csv', index=False)

# Initialize budget
budget_data = {
    'category': ['Rent', 'Dates', 'Food', 'Other'],
    'amount': [500, 200, 0, 0],  # Per pay period
    'period': ['biweekly', 'monthly', 'biweekly', 'biweekly']
}
pd.DataFrame(budget_data).to_csv('data/budget.csv', index=False)

# Initialize transactions with your first paycheck
transactions_data = {
    'date': [datetime.now().strftime('%Y-%m-%d')],
    'amount': [1494],  # Your biweekly salary
    'category': ['Income'],
    'description': ['First paycheck']
}
pd.DataFrame(transactions_data).to_csv('data/transactions.csv', index=False)

print("Data initialized successfully!") 