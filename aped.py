from flask import Flask, render_template, jsonify, request, send_from_directory
from pymongo import MongoClient
import plotly.graph_objects as go
import plotly.io as pio
import os
from dotenv import load_dotenv
import pandas as pd  # Make sure pandas is installed

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI')

# Check if MONGO_URI is loaded correctly
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['database']  # Replace with your database name
    collection = db['coal']  # Replace with your collection name
    print("MongoDB connection successful")
except Exception as e:
    raise ConnectionError(f"Error connecting to MongoDB: {e}")

# Serve the index.html file
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Serve other static files (CSS, JS, images, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Serve the emission.html file
@app.route('/emission')
def serve_emission():
    return send_from_directory('templates', 'demission.html')

@app.route('/getVisualization', methods=['POST'])
def get_visualization():
    mine_name = request.json.get('mineName')
    if not mine_name:
        return jsonify({'error': 'Mine name is required'}), 400

    # Fetch mine data from MongoDB
    mine = collection.find_one({'Mine Name': mine_name})
    if not mine:
        return jsonify({'error': 'Mine not found'}), 404

    # Prepare data for visualization
    data = {
        'Excavation Volume': mine.get('Excavation Volume (tons)', 0),
        'Fuel Consumption': mine.get('Fuel Consumption (liters)', 0),
        'Energy Consumption': mine.get('Energy Consumption (kWh)', 0),
        'Annual Production': mine.get('Annual Production (tons)', 0),
    }
    df = pd.DataFrame(list(data.items()), columns=['Metric', 'Value'])

    # Create Bar Chart
    bar_fig = go.Figure(data=[go.Bar(x=df['Metric'], y=df['Value'])])
    bar_fig.update_layout(title=f"Data for {mine_name}", xaxis_title='Metric', yaxis_title='Value')

    # Create Pie Chart
    pie_fig = go.Figure(data=[go.Pie(labels=df['Metric'], values=df['Value'])])
    pie_fig.update_layout(title=f"Distribution of Metrics for {mine_name}")

    # Save Plotly figures as HTML
    bar_plotly_file = os.path.join('static', 'mine_bar_visualization.html')
    pie_plotly_file = os.path.join('static', 'mine_pie_visualization.html')
    
    pio.write_html(bar_fig, file=bar_plotly_file, auto_open=False)
    pio.write_html(pie_fig, file=pie_plotly_file, auto_open=False)

    # Return URLs to the frontend
    return jsonify({
        'barChartUrl': '/static/mine_bar_visualization.html',
        'pieChartUrl': '/static/mine_pie_visualization.html'
    })

@app.route('/calculateEmissions', methods=['POST'])
def calculate_emissions():
    data = request.json
    excavation_data = float(data.get('excavationData', 0))
    transportation_data = float(data.get('transportationData', 0))
    equipment_data = float(data.get('equipmentData', 0))

    # Define emission factors (use real values from your application)
    emission_factors = {
        'excavation': 0.03,  # kg CO2 per ton
        'transportation': 0.3,  # kg CO2 per km
        'equipment': 0.85  # kg CO2 per kWh (assume 1 hour = 1 kWh for simplicity)
    }

    # Calculate emissions
    excavation_emissions = excavation_data * emission_factors['excavation']
    transportation_emissions = transportation_data * emission_factors['transportation']
    equipment_emissions = equipment_data * emission_factors['equipment']

    total_emissions = excavation_emissions + transportation_emissions + equipment_emissions

    # Prepare data for visualizations
    data_for_bar_chart = {
        'Excavation': excavation_emissions,
        'Transportation': transportation_emissions,
        'Equipment': equipment_emissions
    }

    data_for_pie_chart = {
        'Excavation': excavation_emissions,
        'Transportation': transportation_emissions,
        'Equipment': equipment_emissions
    }

    # Bar chart
    df_bar = pd.DataFrame(list(data_for_bar_chart.items()), columns=['Category', 'Emissions'])
    fig_bar = go.Figure(data=[go.Bar(x=df_bar['Category'], y=df_bar['Emissions'])])
    fig_bar.update_layout(title="Emission Breakdown by Category", xaxis_title='Category', yaxis_title='Emissions (kg CO2)')

    bar_chart_file = os.path.join('static', 'bar_chart.html')
    pio.write_html(fig_bar, file=bar_chart_file, auto_open=False)

    # Pie chart
    fig_pie = go.Figure(data=[go.Pie(labels=list(data_for_pie_chart.keys()), values=list(data_for_pie_chart.values()))])
    fig_pie.update_layout(title="Emission Distribution by Category")

    pie_chart_file = os.path.join('static', 'pie_chart.html')
    pio.write_html(fig_pie, file=pie_chart_file, auto_open=False)

    return jsonify({
        'barChartUrl': '/static/bar_chart.html',
        'pieChartUrl': '/static/pie_chart.html'
    })
    
if __name__ == '__main__':
    app.run(debug=True)
