# Personal AI Accountant

A simple AI-powered personal accounting assistant that helps track expenses, income, and provides financial insights.

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Get your API key from: https://platform.openai.com/api-keys

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and go to `http://localhost:5000`

## Features

- Track income and expenses
- Natural language input for transactions
- Financial insights and recommendations
- Budget tracking
- Savings goals monitoring
- CSV-based data storage

## Data Storage

All financial data is stored in CSV files in the `data` directory:
- `transactions.csv`: All income and expenses
- `goals.csv`: Savings and spending goals
- `budget.csv`: Monthly budget allocations 