from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import json
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize CSV files if they don't exist
def init_csv_files():
    if not os.path.exists('data/transactions.csv'):
        pd.DataFrame(columns=['date', 'amount', 'category', 'description']).to_csv('data/transactions.csv', index=False)
    if not os.path.exists('data/goals.csv'):
        pd.DataFrame(columns=['goal', 'target_amount', 'current_amount', 'deadline']).to_csv('data/goals.csv', index=False)
    if not os.path.exists('data/budget.csv'):
        pd.DataFrame(columns=['category', 'amount', 'period']).to_csv('data/budget.csv', index=False)

init_csv_files()

def process_natural_language(text):
    """Process natural language input using improved rules"""
    try:
        # Extract amount using regex
        amount_match = re.search(r'\$?\d+(?:\.\d{2})?', text)
        if not amount_match:
            return None
        amount = float(amount_match.group().replace('$', ''))

        # Lowercase text for easier matching
        lower_text = text.lower()

        # Determine if it's an expense, income, or savings
        is_expense = any(word in lower_text for word in [
            'spent', 'paid', 'cost', 'bought', 'purchase', 'pay for', 'charged', 'gave', 'owe', 'due', 'bill', 'rent', 'trip', 'gift', 'date', 'shopping', 'food', 'restaurant', 'groceries', 'subscription', 'fee', 'ticket', 'monthly', 'credit', 'loan', 'withdraw', 'transfer to', 'sent to', 'donation', 'donated', 'contributed', 'contribution', 'lost', 'fine', 'penalty', 'parking', 'transport', 'bus', 'train', 'taxi', 'uber', 'lyft', 'gas', 'fuel', 'movie', 'theatre', 'concert', 'game', 'entertainment', 'store', 'mall', 'clothes', 'clothing', 'utility', 'electricity', 'water', 'internet', 'phone', 'housing', 'apartment', 'house'])
        is_income = any(word in lower_text for word in [
            'salary', 'paycheck', 'income', 'earned', 'received', 'got paid', 'deposit', 'deposited', 'bonus', 'refund', 'reimbursement', 'interest', 'dividend', 'won', 'gifted', 'prize', 'reward', 'cashback', 'transfer from', 'received from', 'allowance', 'stipend', 'scholarship', 'grant', 'loan received', 'payment from', 'sold', 'sale', 'profit', 'commission', 'tips', 'tip', 'wage', 'income'])
        is_saving = any(word in lower_text for word in [
            'save', 'saved', 'put in', 'put into', 'added to', 'add to', 'deposit to', 'deposited to', 'transfer to savings', 'set aside', 'set to', 'put towards', 'put toward', 'contribute to', 'contributed to', 'fund', 'funded', 'saving for', 'saving towards', 'saving to', 'saving'])

        # If it's a saving, try to extract the goal name
        goal_name = None
        if is_saving:
            # Try to match a goal name from the goals.csv
            goals_df = pd.read_csv('data/goals.csv')
            for goal in goals_df['goal']:
                if goal.lower() in lower_text:
                    goal_name = goal
                    break
            if not goal_name:
                goal_name = 'General Savings'

        # Set amount sign
        if is_expense:
            amount = -abs(amount)
        elif is_income:
            amount = abs(amount)
        elif is_saving:
            # For savings, treat as positive (adding to savings)
            amount = abs(amount)
        else:
            # Default: treat as expense
            amount = -abs(amount)

        # Determine category
        category = "Other"
        description = text
        categories = {
            'Food': ['food', 'restaurant', 'dinner', 'lunch', 'breakfast', 'coffee', 'meal', 'groceries'],
            'Transportation': ['transport', 'bus', 'train', 'taxi', 'uber', 'lyft', 'gas', 'fuel'],
            'Entertainment': ['movie', 'theatre', 'concert', 'game', 'entertainment'],
            'Shopping': ['shopping', 'store', 'mall', 'clothes', 'clothing'],
            'Bills': ['bill', 'utility', 'electricity', 'water', 'internet', 'phone', 'subscription', 'fee'],
            'Rent': ['rent', 'housing', 'apartment', 'house'],
            'Income': ['salary', 'paycheck', 'income', 'earned', 'received', 'deposit', 'bonus', 'refund', 'reimbursement', 'interest', 'dividend', 'won', 'gifted', 'prize', 'reward', 'cashback', 'allowance', 'stipend', 'scholarship', 'grant', 'loan received', 'payment from', 'sold', 'sale', 'profit', 'commission', 'tips', 'tip', 'wage'],
            'Savings': ['save', 'saved', 'put in', 'put into', 'added to', 'add to', 'deposit to', 'deposited to', 'transfer to savings', 'set aside', 'set to', 'put towards', 'put toward', 'contribute to', 'contributed to', 'fund', 'funded', 'saving for', 'saving towards', 'saving to', 'saving']
        }
        for cat, keywords in categories.items():
            if any(keyword in lower_text for keyword in keywords):
                category = cat
                break
        if is_saving:
            category = 'Savings'
            description = f"{text} (Goal: {goal_name})"

        return {
            'amount': amount,
            'category': category,
            'description': description,
            'goal_name': goal_name if is_saving else None
        }
    except Exception as e:
        print(f"Error processing text: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/transaction', methods=['POST'])
def add_transaction():
    data = request.json
    text = data.get('text', '')
    processed_data = process_natural_language(text)
    if not processed_data:
        return jsonify({'error': 'Could not process the input'}), 400

    # Add transaction to CSV
    df = pd.read_csv('data/transactions.csv')
    new_row = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'amount': processed_data['amount'],
        'category': processed_data['category'],
        'description': processed_data['description']
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('data/transactions.csv', index=False)

    # If it's a saving, update the goal
    if processed_data.get('goal_name'):
        goals_df = pd.read_csv('data/goals.csv')
        mask = goals_df['goal'] == processed_data['goal_name']
        if mask.any():
            goals_df.loc[mask, 'current_amount'] += abs(processed_data['amount'])
            goals_df.to_csv('data/goals.csv', index=False)

    return jsonify({'message': 'Transaction added successfully'})

@app.route('/api/summary', methods=['GET'])
def get_summary():
    transactions_df = pd.read_csv('data/transactions.csv')
    goals_df = pd.read_csv('data/goals.csv')
    total_income = float(transactions_df[transactions_df['amount'] > 0]['amount'].sum())
    total_expenses = float(abs(transactions_df[transactions_df['amount'] < 0]['amount'].sum()))
    net_balance = float(total_income - total_expenses)
    category_expenses = transactions_df[transactions_df['amount'] < 0].groupby('category')['amount'].sum().abs().to_dict()
    category_expenses = {k: float(v) for k, v in category_expenses.items()}
    today = datetime.now()
    savings_goals = []
    for _, goal in goals_df.iterrows():
        deadline = datetime.strptime(goal['deadline'], '%Y-%m-%d')
        days_remaining = (deadline - today).days
        if days_remaining > 0:
            remaining_amount = float(goal['target_amount']) - float(goal['current_amount'])
            daily_savings_needed = remaining_amount / days_remaining
            biweekly_savings_needed = daily_savings_needed * 14
            savings_goals.append({
                'goal': goal['goal'],
                'target_amount': float(goal['target_amount']),
                'current_amount': float(goal['current_amount']),
                'remaining_amount': remaining_amount,
                'days_remaining': days_remaining,
                'daily_savings_needed': round(daily_savings_needed, 2),
                'biweekly_savings_needed': round(biweekly_savings_needed, 2)
            })
    # Always send savings_goals, even if empty
    return jsonify({
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'category_expenses': category_expenses,
        'savings_goals': savings_goals
    })

@app.route('/api/update_goal', methods=['POST'])
def update_goal():
    data = request.json
    goal_name = data.get('goal')
    amount = float(data.get('amount', 0))
    
    # Read goals
    goals_df = pd.read_csv('data/goals.csv')
    
    # Update the goal
    mask = goals_df['goal'] == goal_name
    if mask.any():
        goals_df.loc[mask, 'current_amount'] += amount
        goals_df.to_csv('data/goals.csv', index=False)
        return jsonify({'message': f'Updated {goal_name} goal successfully'})
    
    return jsonify({'error': 'Goal not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 