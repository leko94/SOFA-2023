import logging
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import smtplib
from email.message import EmailMessage

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')
server = app.server  # Expose the server for WSGI

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Function to send email
def send_email(message_content):
    msg = EmailMessage()
    msg.set_content(message_content)
    msg['Subject'] = "New Message from SOFA 2024 Dashboard"
    msg['From'] = "ngcobo.nkululeko@yahoo.com"  # Replace with your email
    msg['To'] = "213524994@stu.ukzn.ac.za"  # Replace with recipient email

    # Send the email
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with actual SMTP server details
            server.starttls()
            server.login("your_email@example.com", "your_password")  # Replace with your email credentials
            server.send_message(msg)
        return "Message sent successfully!"
    except Exception as e:
        return f"Error sending message: {str(e)}"

# Dropdown options for each tab
tab1_options = [
    {'label': "(2019-2023) Number Of Permanent Academic Staff", 'value': '1'},
    {'label': "(2019-2023) Number of Staff with PhD", 'value': '2'},
    {'label': "(2019-2023) Percentage Female Permanent Academic Staff", 'value': '3'},
    {'label': "(2019-2023) Number of Staff with PhD", 'value': '4'},
    {'label': "(2019-2023) Percentage Permanent African Staff", 'value': '5'},
    {'label': "(2019-2023) Percentage of Academic Staff by Department", 'value': '6'}
]

tab2_options = [
    {'label': "(2020-2023) Headcount Enrollment: Planned Vs Achieved", 'value': '7a'},
    {'label': "2023 FAS Planned, Actual, and Difference", 'value': '7b'},
    {'label': "(2019-2023) Percentage of African Students", 'value': '7'},
    {'label': "(2019-2023) Percentage Female Students", 'value': '8'},
    {'label': "(2019-2023) FAS Postgraduate Enrolment", 'value': '9'},
    {'label': "(2020-2023) Postgraduate Enrolment - Actual Students per Department", 'value': '10'},
    {'label': "2023 FAS Student Enrolment by Level", 'value': '11'}
]

tab3_options = [
    {'label': "(2019-2023) FAS Overall Student Success Rates", 'value': '12'},
    {'label': "(2019-2023) Percentage Success Rates by Department", 'value': '13'},
    {'label': "(2019-2023) Success Rates of First Time Entering Students", 'value': '14'},
    {'label': "(2019-2023) Success Rates of African Students", 'value': '15'},
    {'label': "(2019-2023) Faculty Student Throughput - Undergraduate", 'value': '16'},
    {'label': "(2019-2023) Percentage of Student Throughput by Department - Undergraduate", 'value': '17'},
    {'label': "(2019-2023) Percentage Student Dropout Rates - Undergraduate", 'value': '18'},
    {'label': "(2023) Undergraduate Dropout VS Throughput VS Still in Progress", 'value': '19'},
    {'label': "(2020-2023) Percentage for FAS Graduation Rates", 'value': '20'},
    {'label': "(2019-2023) Graduation Rates by Programme", 'value': '21'},
    {'label': "(2019-2023) Percentage for Postgraduate Graduation Rates", 'value': '22'},
    {'label': "(2019-2023) Pass Rates by Program", 'value': '23'}
]

# Layout for each tab content
tab1_content = html.Div([
    dcc.Dropdown(id="tab1-dropdown", options=tab1_options, placeholder="Select an option", className="mb-3"),
    html.Div(id="tab1-image-container")  # Container for image display
])

tab2_content = html.Div([
    dcc.Dropdown(id="tab2-dropdown", options=tab2_options, placeholder="Select an option", className="mb-3"),
    html.Div(id="tab2-image-container")  # Container for image display
])

tab3_content = html.Div([
    dcc.Dropdown(id="tab3-dropdown", options=tab3_options, placeholder="Select an option", className="mb-3"),
    html.Div(id="tab3-image-container")  # Container for image display
])

# Define Tabs
tabs = dbc.Tabs([
    dbc.Tab(tab1_content, label="Staff Profile Status"),
    dbc.Tab(tab2_content, label="Student Enrolment Status"),
    dbc.Tab(tab3_content, label="Student Progress Indicators")
])

# Chat box layout
chat_box = html.Div([
    html.H5("Contact Us"),
    dcc.Textarea(id='message-box', placeholder="Type your message here...", style={'width': '100%', 'height': 100}),
    html.Br(),
    dbc.Button("Send", id="send-button", color="primary", className="mt-2"),
    html.Div(id="response-message", className="mt-2")
])

# Main layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("SOFA 2024", style={'text-align': 'left', 'font-size': '3em'}), width=9),
        dbc.Col(html.Img(src="assets/Logo1.png", style={'width': '100%', 'height': '50%'}), width=3),
    ], className="mt-4 mb-4"),
    dbc.Row([
        dbc.Col([
            tabs,
            html.Hr(),
            chat_box
        ])
    ])
])

# Callbacks to display images based on dropdown selection
@app.callback(
    Output("tab1-image-container", "children"),
    [Input("tab1-dropdown", "value")]
)
def display_tab1_image(selected_value):
    if selected_value:
        return html.Img(src=f"/assets/{selected_value}.png", style={'width': '50%', 'height': '50%'})
    return ""

@app.callback(
    Output("tab2-image-container", "children"),
    [Input("tab2-dropdown", "value")]
)
def display_tab2_image(selected_value):
    if selected_value:
        return html.Img(src=f"/assets/{selected_value}.png", style={'width': '50%', 'height': '50%'})
    return ""

@app.callback(
    Output("tab3-image-container", "children"),
    [Input("tab3-dropdown", "value")]
)
def display_tab3_image(selected_value):
    if selected_value:
        return html.Img(src=f"/assets/{selected_value}.png", style={'width': '50%', 'height': '50%'})
    return ""

# Callback for the chat box
@app.callback(
    Output("response-message", "children"),
    [Input("send-button", "n_clicks")],
    [State("message-box", "value")]
)
def send_message(n_clicks, message_content):
    if n_clicks:
        if message_content:
            response = send_email(message_content)
            return response
        else:
            return "Please enter a message before sending."
    return ""

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=False, port=8050)  # debug=False for production
