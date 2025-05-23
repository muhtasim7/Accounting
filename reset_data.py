import pandas as pd
import os

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Reset transactions
transactions_df = pd.DataFrame(columns=['date', 'amount', 'category', 'description'])
transactions_df.to_csv('data/transactions.csv', index=False)

# Reset goals
goals_df = pd.DataFrame({
    'goal': ['Summer Savings', 'Trip', 'Gifts', 'Monthly Dates'],
    'target_amount': [3000, 2000, 1000, 2400],
    'current_amount': [0, 0, 0, 0],
    'deadline': ['2024-08-22', '2024-08-22', '2024-08-22', '2024-05-23']
})
goals_df.to_csv('data/goals.csv', index=False)

# Reset budget
budget_df = pd.DataFrame({
    'category': ['Rent', 'Dates', 'Food', 'Other'],
    'amount': [500, 200, 0, 0],
    'period': ['biweekly', 'monthly', 'biweekly', 'biweekly']
})
budget_df.to_csv('data/budget.csv', index=False)

print("All data has been reset to initial state!") 