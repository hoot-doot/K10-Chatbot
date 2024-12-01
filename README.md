## Overview
###The Financial Chatbot is a Python-based application designed to provide financial insights about companies based on data from a CSV file. It is integrated into a Flask web application for user interaction via a chat interface. The chatbot processes user queries and provides concise, relevant financial data.

#### How It Works
1.Data Loading and Preprocessing:

Reads financial data from a CSV file (k10_trends.csv).
Extracts company-specific data and organizes it for efficient querying.


2.Query Processing:

Listens for user input via the /chat API endpoint.
Matches the query against predefined patterns to identify the requested financial information.
Retrieves the relevant data from the processed dataset and formats it into a response.


3.Web Integration:

A Flask web application renders a user interface (index.html) for chat interaction.
JSON queries are sent to the chatbot, and responses are returned in real-time.

#### Limitations
1. Data Scope: The chatbot only provides information about companies included in the CSV file (e.g., Apple, Microsoft, Tesla).
2. Query Flexibility: Responses are limited to predefined topics (total revenue, net income, and cash flow). It may not understand complex or unrelated queries.
3. Static Data: Insights are based on the data in the CSV file, which needs regular updates to stay current.
4. No Predictive Analytics: The chatbot does not perform forecasting or predictive analysis.
