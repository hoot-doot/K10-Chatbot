import pandas as pd
from flask import Flask, render_template, request, jsonify
import json

class FinancialChatbot:
    def __init__(self, csv_file):
        """
        Initialize the chatbot with financial data from the CSV file.
        
        Args:
            csv_file (str): Path to the CSV file containing financial data
        """
        # Read the CSV file
        self.df = pd.read_csv(csv_file)
        
        # Preprocess the data for easier querying
        self.latest_data = self.df.iloc[-1]  # Most recent row
        self.companies = self.df['Company'].unique()
        
        # Prepare company-specific data dictionary
        self.company_data = {}
        for company in self.companies:
            company_rows = self.df[self.df['Company'] == company]
            self.company_data[company] = {
                'latest_year': company_rows['Year'].max(),
                'revenues': company_rows['Total Revenue'].tolist(),
                'net_incomes': company_rows['Net Income'].tolist(),
                'years': company_rows['Year'].tolist()
            }
    
    def process_query(self, query):
        """
        Process user queries and return appropriate responses.
        
        Args:
            query (str): User's input query
        
        Returns:
            str: Chatbot's response
        """
        # Convert query to lowercase for case-insensitive matching
        query = query.lower()
        
        # Company-specific queries
        for company in self.companies:
            if company.lower() in query:
                return self._handle_company_query(company, query)
        
        # General financial queries
        if any(phrase in query for phrase in ['total revenue', 'revenue']):
            return self._get_total_revenue_info()
        
        if any(phrase in query for phrase in ['net income', 'profit']):
            return self._get_net_income_info()
        
        if any(phrase in query for phrase in ['cash flow', 'cashflow']):
            return self._get_cash_flow_info()
        
        # Catch-all response
        return "I'm sorry, I can only provide information about total revenue, net income, and cash flow for Apple, Microsoft, and Tesla. Could you rephrase your query?"
    
    def _handle_company_query(self, company, query):
        """
        Handle queries specific to a particular company.
        """
        data = self.company_data[company]
        latest_year = data['latest_year']
        
        company_row = self.df[(self.df['Company'] == company) & (self.df['Year'] == latest_year)].iloc[0]
        
        if 'revenue' in query:
            return f"{company}'s latest total revenue is ${company_row['Total Revenue']:,} with a growth rate of {company_row['Total Revenue Growth (%)']:.2f}%."
        
        if 'net income' in query or 'profit' in query:
            return f"{company}'s latest net income is ${company_row['Net Income']:,} with a growth rate of {company_row['Net Income Growth (%)']:.2f}%."
        
        if 'cash flow' in query:
            return f"{company}'s latest cash flow is ${company_row['Cash Flow']:,} with a growth rate of {company_row['Cash Flow Growth (%)']:.2f}%."
        
        return f"I have financial information about {company}, but could you be more specific?"
    
    def _get_total_revenue_info(self):
        """
        Provide overall total revenue information.
        """
        latest_row = self.df.iloc[-1]
        return f"The latest total revenue is ${latest_row['Total Revenue']:,} with a growth rate of {latest_row['Total Revenue Growth (%)']:.2f}%."
    
    def _get_net_income_info(self):
        """
        Provide overall net income information.
        """
        latest_row = self.df.iloc[-1]
        return f"The latest net income is ${latest_row['Net Income']:,} with a growth rate of {latest_row['Net Income Growth (%)']:.2f}%."
    
    def _get_cash_flow_info(self):
        """
        Provide overall cash flow information.
        """
        latest_row = self.df.iloc[-1]
        return f"The latest cash flow is ${latest_row['Cash Flow']:,} with a growth rate of {latest_row['Cash Flow Growth (%)']:.2f}%."

# Flask Application
app = Flask(__name__)
chatbot = FinancialChatbot('k10_trends.csv')

@app.route('/')
def index():
    """
    Render the main chatbot interface.
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat requests and return bot responses.
    """
    data = request.get_json()
    query = data.get('query', '')
    
    response = chatbot.process_query(query)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)