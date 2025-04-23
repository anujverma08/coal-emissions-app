from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import plotly.graph_objects as go
import plotly.io as pio
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the .env file")

try:
    client = MongoClient(MONGO_URI)
    db = client['database']
    collection = db['coal']
    print("MongoDB connection successful")
except Exception as e:
    raise ConnectionError(f"Error connecting to MongoDB: {e}")

# Homepage
@app.route('/')
def serve_index():
    return render_template('index.html')

# Dynamic HTML pages from templates folder
@app.route('/<page>.html')
def serve_pages(page):
    try:
        return render_template(f'{page}.html')
    except:
        return "Page not found", 404

# Specific route for emission page
@app.route('/emission')
def serve_emission():
    return render_template('demission.html')

# Route for generating visualizations
@app.route('/getVisualization', methods=['POST'])
def get_visualization():
    mine_name = request.json.get('mineName')
    if not mine_name:
        return jsonify({'error': 'Mine name is required'}), 400

    mine = collection.find_one({'Mine Name': mine_name})
    if not mine:
        return jsonify({'error': 'Mine not found'}), 404

    data = {
        'Excavation Volume': mine.get('Excavation Volume (tons)', 0),
        'Fuel Consumption': mine.get('Fuel Consumption (liters)', 0),
        'Energy Consumption': mine.get('Energy Consumption (kWh)', 0),
    }

    df = pd.DataFrame(list(data.items()), columns=['Metric', 'Value'])

    # Bar Chart
    bar_fig = go.Figure(data=[go.Bar(x=df['Metric'], y=df['Value'])])
    bar_fig.update_layout(title=f"Data for {mine_name}", xaxis_title='Metric', yaxis_title='Value')

    # Pie Chart
    pie_fig = go.Figure(data=[go.Pie(labels=df['Metric'], values=df['Value'])])
    pie_fig.update_layout(title=f"Distribution of Metrics for {mine_name}")

    bar_file = os.path.join('static', 'mine_bar_visualization.html')
    pie_file = os.path.join('static', 'mine_pie_visualization.html')

    pio.write_html(bar_fig, file=bar_file, auto_open=False)
    pio.write_html(pie_fig, file=pie_file, auto_open=False)

    return jsonify({
        'barChartUrl': '/static/mine_bar_visualization.html',
        'pieChartUrl': '/static/mine_pie_visualization.html'
    })

# Route for real-time emission calculation
@app.route('/calculateEmissions', methods=['POST'])
def calculate_emissions():
    data = request.json
    excavation_data = float(data.get('excavationData', 0))
    transportation_data = float(data.get('transportationData', 0))
    equipment_data = float(data.get('equipmentData', 0))

    emission_factors = {
        'excavation': 0.03,
        'transportation': 0.3,
        'equipment': 0.85
    }

    excavation_emissions = excavation_data * emission_factors['excavation']
    transportation_emissions = transportation_data * emission_factors['transportation']
    equipment_emissions = equipment_data * emission_factors['equipment']
    total_emissions = excavation_emissions + transportation_emissions + equipment_emissions

    data_for_charts = {
        'Excavation': excavation_emissions,
        'Transportation': transportation_emissions,
        'Equipment': equipment_emissions
    }

    max_category = max(data_for_charts, key=data_for_charts.get)
    max_value = data_for_charts[max_category]

    if max_category == 'Excavation':
        inference = f"Excavation is the largest contributor to your emissions with {max_value:.2f} kg CO2. Consider optimizing excavation practices or using more energy-efficient equipment."
    elif max_category == 'Transportation':
        inference = f"Transportation is the largest contributor to your emissions with {max_value:.2f} kg CO2. You could reduce emissions by improving logistics or using more efficient vehicles."
    else:
        inference = f"Equipment usage is the largest contributor to your emissions with {max_value:.2f} kg CO2. You can reduce emissions by upgrading to more energy-efficient machinery."

    df_bar = pd.DataFrame(list(data_for_charts.items()), columns=['Category', 'Emissions'])
    fig_bar = go.Figure(data=[go.Bar(x=df_bar['Category'], y=df_bar['Emissions'])])
    fig_bar.update_layout(title="Emission Breakdown by Category", xaxis_title='Category', yaxis_title='Emissions (kg CO2)')

    bar_chart_file = os.path.join('static', 'bar_chart.html')
    pie_chart_file = os.path.join('static', 'pie_chart.html')

    pio.write_html(fig_bar, file=bar_chart_file, auto_open=False)

    fig_pie = go.Figure(data=[go.Pie(labels=list(data_for_charts.keys()), values=list(data_for_charts.values()))])
    fig_pie.update_layout(title="Emission Distribution by Category")
    pio.write_html(fig_pie, file=pie_chart_file, auto_open=False)

    return jsonify({
        'barChartUrl': '/static/bar_chart.html',
        'pieChartUrl': '/static/pie_chart.html',
        'inference': inference
    })

if __name__ == '__main__':
    app.run(debug=True)
