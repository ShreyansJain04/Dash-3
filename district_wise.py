# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import dash
# from dash import dcc, html, Input, Output, State
# import dash_bootstrap_components as dbc

# # Load data
# df = pd.read_excel('C:\\Users\\Vidhi Shah\\Downloads\\Updated_Transprioritybase (1).xlsx')

# # Get unique states and state-district mapping
# states = sorted(df['State'].dropna().unique())
# state_districts = {}
# for state in states:
#     state_districts[state] = sorted(df[df['State'] == state]['District Name'].dropna().unique())

# # Color scheme for priorities
# priority_colors = {
#     'P1': '#28a745', 'P2': '#17a2b8', 'P3': '#ffc107', 'P4': '#dc3545'
# }

# # Initialize Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Main navigation component
# def create_navbar():
#     return dbc.Navbar([
#         dbc.NavbarBrand("🏭 State-wise Customer Analytics", href="/", className="ml-2"),
#         dbc.Nav([
#             dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
#         ], navbar=True),
#     ], color="dark", dark=True, className="mb-4")

# # Main page layout - State selection
# def create_main_page():
#     return dbc.Container([
#         dbc.Row([
#             dbc.Col([
#                 html.H2("Select a State", className="text-center mb-4"),
#                 html.P("Choose a state to view district-wise analytics", className="text-center text-muted mb-4")
#             ])
#         ]),
        
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         dbc.Button(
#                             state, 
#                             href=f"/state/{state}",
#                             color="primary",
#                             size="lg",
#                             className="mb-3 w-100",
#                             style={'height': '60px', 'fontSize': '18px'}
#                         )
#                     ])
#                 ], className="mb-3")
#             ], width=6, lg=4) for state in states
#         ])
#     ])

# # State page layout - District selection
# def create_state_page(state_name):
#     if state_name not in state_districts:
#         return html.Div("State not found")
    
#     districts = state_districts[state_name]
#     state_data = df[df['State'] == state_name]
    
#     # State overview stats
#     total_customers = len(state_data)
#     p1_customers = len(state_data[state_data['Priority'] == 'P1'])
#     avg_volume = state_data['Order vol / month'].mean()
    
#     return dbc.Container([
#         dbc.Row([
#             dbc.Col([
#                 html.H2(f"{state_name} - District Selection", className="mb-3"),
#                 html.P(f"Select a district to view detailed analytics", className="text-muted mb-4")
#             ])
#         ]),
        
#         # State overview cards
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4(f"{total_customers:,}", className="text-primary"),
#                         html.P("Total Customers", className="mb-0")
#                     ])
#                 ], className="text-center")
#             ], width=4),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4(f"{p1_customers:,}", className="text-success"),
#                         html.P("P1 Customers", className="mb-0")
#                     ])
#                 ], className="text-center")
#             ], width=4),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4(f"{avg_volume:.1f}", className="text-info"),
#                         html.P("Avg Volume/Month", className="mb-0")
#                     ])
#                 ], className="text-center")
#             ], width=4)
#         ], className="mb-4"),
        
#         # District buttons
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         dbc.Button(
#                             district,
#                             href=f"/analytics/{state_name}/{district}",
#                             color="outline-primary",
#                             size="md",
#                             className="mb-2 w-100",
#                             style={'height': '50px'}
#                         )
#                     ])
#                 ])
#             ], width=6, lg=4) for district in districts
#         ])
#     ])

# # Analytics page layout
# def create_analytics_page(state_name, district_name):
#     district_data = df[(df['State'] == state_name) & (df['District Name'] == district_name)]
    
#     if district_data.empty:
#         return html.Div("No data found for this district")
    
#     # Calculate metrics
#     total_customers = len(district_data)
#     priority_counts = district_data['Priority'].value_counts()
#     avg_volume = district_data['Order vol / month'].mean()
#     total_volume = district_data['Order vol / month'].sum()
    
#     # Create visualizations
#     # Priority Distribution Pie Chart
#     fig_priority = px.pie(
#         values=priority_counts.values,
#         names=priority_counts.index,
#         title="Priority Distribution",
#         color=priority_counts.index,
#         color_discrete_map=priority_colors
#     )
#     fig_priority.update_layout(height=400)
    
#     # Volume Distribution Box Plot
#     fig_volume = px.box(
#         district_data,
#         x='Priority',
#         y='Order vol / month',
#         color='Priority',
#         title="Order Volume by Priority",
#         color_discrete_map=priority_colors
#     )
#     fig_volume.update_layout(height=400)
    
#     # Scatter plot: Order Frequency vs Volume
#     fig_scatter = px.scatter(
#         district_data,
#         x='Order # / month',
#         y='Order vol / month',
#         color='Priority',
#         size='Order month #',
#         title="Order Frequency vs Volume",
#         color_discrete_map=priority_colors,
#         hover_data=['Company GSTIN']
#     )
#     fig_scatter.update_layout(height=400)
    
#     return dbc.Container([
#         dbc.Row([
#             dbc.Col([
#                 html.H2(f"{district_name}, {state_name} - Analytics", className="mb-3"),
#                 dbc.Breadcrumb(items=[
#                     {"label": "Home", "href": "/"},
#                     {"label": state_name, "href": f"/state/{state_name}"},
#                     {"label": district_name, "active": True}
#                 ])
#             ])
#         ]),
        
#         # KPI Cards
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4(f"{total_customers:,}", className="text-primary"),
#                         html.P("Total Customers")
#                     ])
#                 ], className="text-center")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4(f"{priority_counts.get('P1', 0):,}", className="text-success"),
#                         html.P("P1 Customers")
#                     ])
#                 ], className="text-center")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4(f"{avg_volume:.1f}", className="text-info"),
#                         html.P("Avg Volume/Month")
#                     ])
#                 ], className="text-center")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.H4(f"{total_volume:.0f}", className="text-warning"),
#                         html.P("Total Volume")
#                     ])
#                 ], className="text-center")
#             ], width=3)
#         ], className="mb-4"),
        
#         # Charts Row 1
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(figure=fig_priority)
#             ], width=6),
#             dbc.Col([
#                 dcc.Graph(figure=fig_volume)
#             ], width=6)
#         ], className="mb-4"),
        
#         # Charts Row 2
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(figure=fig_scatter)
#             ], width=12)
#         ], className="mb-4"),
        
#         # Customer Table
#         dbc.Row([
#             dbc.Col([
#                 html.H4("Customer Details"),
#                 dbc.Table.from_dataframe(
#                     district_data[['Company GSTIN', 'Priority', 'Order vol / month', 'Order # / month']].head(10),
#                     striped=True, bordered=True, hover=True, size='sm'
#                 )
#             ])
#         ])
#     ])

# # Main app layout with URL routing
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     create_navbar(),
#     html.Div(id='page-content')
# ])

# # Callback for page routing
# @app.callback(
#     Output('page-content', 'children'),
#     Input('url', 'pathname')
# )
# def display_page(pathname):
#     if pathname == '/' or pathname is None:
#         return create_main_page()
#     elif pathname.startswith('/state/'):
#         state_name = pathname.split('/')[-1]
#         return create_state_page(state_name)
#     elif pathname.startswith('/analytics/'):
#         parts = pathname.split('/')
#         if len(parts) >= 4:
#             state_name = parts[2]
#             district_name = parts[3]
#             return create_analytics_page(state_name, district_name)
    
#     return html.Div("404 - Page not found")

# if __name__ == '__main__':
#     app.run_server(debug=True)





# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import dash
# from dash import dcc, html, Input, Output, State
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate
# import numpy as np
# from datetime import datetime

# # Load and preprocess data
# try:
#     df = pd.read_excel('C:\\Users\\Vidhi Shah\\Downloads\\Updated_Transprioritybase (1).xlsx')
    
#     # Data preprocessing
#     df['Order vol / month'] = pd.to_numeric(df['Order vol / month'], errors='coerce')
#     df['Order # / month'] = pd.to_numeric(df['Order # / month'], errors='coerce')
#     df['Order month #'] = pd.to_numeric(df['Order month #'], errors='coerce')
    
#     # Get unique states and state-district mapping
#     states = sorted(df['State'].dropna().unique())
#     state_districts = {}
#     for state in states:
#         state_districts[state] = sorted(df[df['State'] == state]['District Name'].dropna().unique())
# except Exception as e:
#     print(f"Error loading data: {e}")
#     df = pd.DataFrame()
#     states = []
#     state_districts = {}

# # Color scheme for priorities
# priority_colors = {
#     'P1': '#2ecc71',  # Emerald
#     'P2': '#3498db',  # Blue
#     'P3': '#f1c40f',  # Yellow
#     'P4': '#e74c3c'   # Red
# }

# # Initialize Dash app
# app = dash.Dash(
#     __name__,
#     external_stylesheets=[
#         dbc.themes.BOOTSTRAP,
#         'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
#     ],
#     meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
# )

# # Navbar component
# def create_navbar():
#     return dbc.Navbar(
#         dbc.Container([
#             dbc.Row([
#                 dbc.Col([
#                     dbc.NavbarBrand([
#                         html.I(className="fas fa-industry me-2"),
#                         "State-wise Customer Analytics"
#                     ], href="/", className="fs-4")
#                 ]),
#                 dbc.Col([
#                     dbc.Input(
#                         type="search",
#                         placeholder="Search customer...",
#                         id="search-input",
#                         className="form-control"
#                     )
#                 ], width=4),
#                 dbc.Col([
#                     dbc.Button(
#                         [
#                             html.I(className="fas fa-download me-2"),
#                             "Export Data"
#                         ],
#                         id="export-button",
#                         color="light",
#                         className="ms-2"
#                     )
#                 ], width="auto")
#             ], className="w-100")
#         ]),
#         color="dark",
#         dark=True,
#         className="mb-4 shadow-sm"
#     )

# # Main page component
# def create_main_page():
#     if df.empty:
#         return html.Div("No data available")
    
#     # Calculate overall statistics
#     total_customers = len(df)
#     total_volume = df['Order vol / month'].sum()
#     avg_volume = df['Order vol / month'].mean()
#     p1_customers = len(df[df['Priority'] == 'P1'])
    
#     return dbc.Container([
#         # Welcome section
#         dbc.Row([
#             dbc.Col([
#                 html.H1("Welcome to Customer Analytics Dashboard", className="text-center mb-4"),
#                 html.P("Select a state to view detailed analytics and insights", className="text-center text-muted mb-5")
#             ])
#         ]),
        
#         # Statistics cards
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-users fa-2x text-primary mb-3"),
#                             html.H3(f"{total_customers:,}", className="text-primary"),
#                             html.P("Total Customers", className="text-muted")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-star fa-2x text-success mb-3"),
#                             html.H3(f"{p1_customers:,}", className="text-success"),
#                             html.P("P1 Customers", className="text-muted")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-chart-line fa-2x text-info mb-3"),
#                             html.H3(f"{avg_volume:.1f}", className="text-info"),
#                             html.P("Avg Volume/Month", className="text-muted")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-box fa-2x text-warning mb-3"),
#                             html.H3(f"{total_volume:,.0f}", className="text-warning"),
#                             html.P("Total Volume", className="text-muted")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3)
#         ], className="mb-5"),
        
#         # State selection grid
#         dbc.Row([
#             dbc.Col([
#                 html.H2("Select a State", className="text-center mb-4")
#             ])
#         ]),
        
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         dbc.Button(
#                             [
#                                 html.I(className="fas fa-map-marker-alt me-2"),
#                                 state
#                             ],
#                             href=f"/state/{state}",
#                             color="primary",
#                             size="lg",
#                             className="w-100",
#                             style={'height': '60px', 'fontSize': '18px'}
#                         )
#                     ])
#                 ], className="shadow-sm mb-4")
#             ], width=6, lg=4) for state in states
#         ])
#     ], fluid=True)

# # State page component
# def create_state_page(state_name):
#     if state_name not in state_districts:
#         return html.Div("State not found")
    
#     districts = state_districts[state_name]
#     state_data = df[df['State'] == state_name]
    
#     # Calculate state-level metrics
#     total_customers = len(state_data)
#     p1_customers = len(state_data[state_data['Priority'] == 'P1'])
#     avg_volume = state_data['Order vol / month'].mean()
#     total_volume = state_data['Order vol / month'].sum()
    
#     # Create state-level visualizations
#     priority_dist = state_data['Priority'].value_counts()
#     fig_priority = px.pie(
#         values=priority_dist.values,
#         names=priority_dist.index,
#         title="Priority Distribution",
#         color=priority_dist.index,
#         color_discrete_map=priority_colors
#     )
#     fig_priority.update_layout(
#         height=400,
#         template="plotly_white",
#         showlegend=True,
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
#     )
    
#     # Volume trend by district
#     district_volumes = state_data.groupby('District Name')['Order vol / month'].mean().sort_values(ascending=False)
#     fig_district_volume = px.bar(
#         x=district_volumes.index,
#         y=district_volumes.values,
#         title="Average Volume by District",
#         labels={'x': 'District', 'y': 'Average Volume'},
#         color=district_volumes.values,
#         color_continuous_scale='Viridis'
#     )
#     fig_district_volume.update_layout(
#         height=400,
#         template="plotly_white",
#         xaxis_tickangle=-45
#     )
    
#     return dbc.Container([
#         # Header with breadcrumb
#         dbc.Row([
#             dbc.Col([
#                 html.H2(f"{state_name} Analytics", className="mb-3"),
#                 dbc.Breadcrumb(
#                     items=[
#                         {"label": "Home", "href": "/"},
#                         {"label": state_name, "active": True}
#                     ],
#                     className="mb-4"
#                 )
#             ])
#         ]),
        
#         # State overview cards
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-users fa-2x text-primary mb-3"),
#                             html.H4(f"{total_customers:,}", className="text-primary"),
#                             html.P("Total Customers", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-star fa-2x text-success mb-3"),
#                             html.H4(f"{p1_customers:,}", className="text-success"),
#                             html.P("P1 Customers", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-chart-line fa-2x text-info mb-3"),
#                             html.H4(f"{avg_volume:.1f}", className="text-info"),
#                             html.P("Avg Volume/Month", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-box fa-2x text-warning mb-3"),
#                             html.H4(f"{total_volume:,.0f}", className="text-warning"),
#                             html.P("Total Volume", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3)
#         ], className="mb-4"),
        
#         # Charts
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(figure=fig_priority)
#             ], width=6),
#             dbc.Col([
#                 dcc.Graph(figure=fig_district_volume)
#             ], width=6)
#         ], className="mb-4"),
        
#         # District selection
#         dbc.Row([
#             dbc.Col([
#                 html.H3("Select a District", className="mb-4")
#             ])
#         ]),
        
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         dbc.Button(
#                             [
#                                 html.I(className="fas fa-map-marker-alt me-2"),
#                                 district
#                             ],
#                             href=f"/analytics/{state_name}/{district}",
#                             color="outline-primary",
#                             size="md",
#                             className="w-100",
#                             style={'height': '50px'}
#                         )
#                     ])
#                 ], className="shadow-sm mb-3")
#             ], width=6, lg=4) for district in districts
#         ])
#     ], fluid=True)

# # Analytics page component
# def create_analytics_page(state_name, district_name):
#     district_data = df[(df['State'] == state_name) & (df['District Name'] == district_name)]
    
#     if district_data.empty:
#         return html.Div("No data found for this district")
    
#     # Calculate metrics
#     total_customers = len(district_data)
#     priority_counts = district_data['Priority'].value_counts()
#     avg_volume = district_data['Order vol / month'].mean()
#     total_volume = district_data['Order vol / month'].sum()
    
#     # Create visualizations
#     fig_priority = px.pie(
#         values=priority_counts.values,
#         names=priority_counts.index,
#         title="Priority Distribution",
#         color=priority_counts.index,
#         color_discrete_map=priority_colors
#     )
#     fig_priority.update_layout(
#         height=400,
#         template="plotly_white",
#         showlegend=True,
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
#     )
    
#     fig_volume = px.box(
#         district_data,
#         x='Priority',
#         y='Order vol / month',
#         color='Priority',
#         title="Order Volume by Priority",
#         color_discrete_map=priority_colors
#     )
#     fig_volume.update_layout(
#         height=400,
#         template="plotly_white",
#         showlegend=False
#     )
    
#     fig_scatter = px.scatter(
#         district_data,
#         x='Order # / month',
#         y='Order vol / month',
#         color='Priority',
#         size='Order month #',
#         title="Order Frequency vs Volume",
#         color_discrete_map=priority_colors,
#         hover_data=['Company GSTIN', 'Order month #'],
#         labels={
#             'Order # / month': 'Orders per Month',
#             'Order vol / month': 'Volume per Month',
#             'Order month #': 'Months Active'
#         }
#     )
#     fig_scatter.update_layout(
#         height=400,
#         template="plotly_white",
#         showlegend=True,
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
#     )
    
#     return dbc.Container([
#         # Header with breadcrumb
#         dbc.Row([
#             dbc.Col([
#                 html.H2(f"{district_name}, {state_name} - Analytics", className="mb-3"),
#                 dbc.Breadcrumb(
#                     items=[
#                         {"label": "Home", "href": "/"},
#                         {"label": state_name, "href": f"/state/{state_name}"},
#                         {"label": district_name, "active": True}
#                     ],
#                     className="mb-4"
#                 )
#             ])
#         ]),
        
#         # KPI Cards
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-users fa-2x text-primary mb-3"),
#                             html.H4(f"{total_customers:,}", className="text-primary"),
#                             html.P("Total Customers", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-star fa-2x text-success mb-3"),
#                             html.H4(f"{priority_counts.get('P1', 0):,}", className="text-success"),
#                             html.P("P1 Customers", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-chart-line fa-2x text-info mb-3"),
#                             html.H4(f"{avg_volume:.1f}", className="text-info"),
#                             html.P("Avg Volume/Month", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardBody([
#                         html.Div([
#                             html.I(className="fas fa-box fa-2x text-warning mb-3"),
#                             html.H4(f"{total_volume:,.0f}", className="text-warning"),
#                             html.P("Total Volume", className="text-muted mb-0")
#                         ], className="text-center")
#                     ])
#                 ], className="shadow-sm h-100")
#             ], width=3)
#         ], className="mb-4"),
        
#         # Charts Row 1
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(figure=fig_priority)
#             ], width=6),
#             dbc.Col([
#                 dcc.Graph(figure=fig_volume)
#             ], width=6)
#         ], className="mb-4"),
        
#         # Charts Row 2
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(figure=fig_scatter)
#             ], width=12)
#         ], className="mb-4"),
        
#         # Customer Table
#         dbc.Row([
#             dbc.Col([
#                 html.H4("Customer Details", className="mb-3"),
#                 dbc.Card([
#                     dbc.CardBody([
#                         dbc.Table.from_dataframe(
#                             district_data[['Company GSTIN', 'Priority', 'Order vol / month', 'Order # / month']].head(10),
#                             striped=True,
#                             bordered=True,
#                             hover=True,
#                             size='sm',
#                             className="table-hover"
#                         )
#                     ])
#                 ], className="shadow-sm")
#             ])
#         ])
#     ], fluid=True)

# # Main app layout
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     create_navbar(),
#     html.Div(id='page-content')
# ])

# # Callback for page routing
# @app.callback(
#     Output('page-content', 'children'),
#     Input('url', 'pathname')
# )
# def display_page(pathname):
#     if pathname == '/' or pathname is None:
#         return create_main_page()
#     elif pathname.startswith('/state/'):
#         state_name = pathname.split('/')[-1]
#         return create_state_page(state_name)
#     elif pathname.startswith('/analytics/'):
#         parts = pathname.split('/')
#         if len(parts) >= 4:
#             state_name = parts[2]
#             district_name = parts[3]
#             return create_analytics_page(state_name, district_name)
    
#     return html.Div("404 - Page not found")

# # Callback for search functionality
# @app.callback(
#     Output('page-content', 'children', allow_duplicate=True),
#     Input('search-input', 'value'),
#     prevent_initial_call=True
# )
# def search_customers(search_term):
#     if not search_term:
#         raise PreventUpdate
    
#     # Search in the dataframe
#     search_results = df[
#         df['Company GSTIN'].str.contains(search_term, case=False, na=False) |
#         df['State'].str.contains(search_term, case=False, na=False) |
#         df['District Name'].str.contains(search_term, case=False, na=False)
#     ]
    
#     if search_results.empty:
#         return html.Div("No results found")
    
#     # Create a results page
#     return dbc.Container([
#         html.H2("Search Results", className="mb-4"),
#         dbc.Table.from_dataframe(
#             search_results[['Company GSTIN', 'State', 'District Name', 'Priority', 'Order vol / month']].head(20),
#             striped=True,
#             bordered=True,
#             hover=True,
#             size='sm'
#         )
#     ])

# if __name__ == '__main__':
#     app.run_server(debug=True)






import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import numpy as np
from datetime import datetime

# Load and preprocess data
try:
    df = pd.read_excel('./Updated_Transprioritybase (1).xlsx')
    
    # Data preprocessing
    df['Order vol / month'] = pd.to_numeric(df['Order vol / month'], errors='coerce')
    df['Order # / month'] = pd.to_numeric(df['Order # / month'], errors='coerce')
    df['Order month #'] = pd.to_numeric(df['Order month #'], errors='coerce')
    
    # Get unique states and state-district mapping
    states = sorted(df['State'].dropna().unique())
    state_districts = {}
    for state in states:
        state_districts[state] = sorted(df[df['State'] == state]['District Name'].dropna().unique())
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()
    states = []
    state_districts = {}

# Dark theme color scheme
dark_colors = {
    'background': '#1a1a1a',
    'card_bg': '#2d2d2d',
    'text': '#ffffff',
    'text_muted': '#b3b3b3',
    'border': '#404040',
    'primary': '#00b4d8',  # Bright blue
    'secondary': '#7209b7',  # Purple
    'success': '#4cc9f0',  # Light blue
    'warning': '#f72585',  # Pink
    'danger': '#ff4d6d'    # Red
}

# Color scheme for priorities
priority_colors = {
    'P1': '#4cc9f0',  # Light blue
    'P2': '#7209b7',  # Purple
    'P3': '#f72585',  # Pink
    'P4': '#ff4d6d'   # Red
}

# Initialize Dash app with dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,  # Using Darkly theme from dash-bootstrap-components
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
    ],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

# Custom CSS for dark theme
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            .card {
                background-color: #2d2d2d !important;
                border: 1px solid #404040 !important;
            }
            .table {
                color: #ffffff !important;
            }
            .table td, .table th {
                border-color: #404040 !important;
            }
            .form-control {
                background-color: #2d2d2d !important;
                border-color: #404040 !important;
                color: #ffffff !important;
            }
            .form-control:focus {
                background-color: #2d2d2d !important;
                border-color: #00b4d8 !important;
                color: #ffffff !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Navbar component
def create_navbar():
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.NavbarBrand([
                        html.I(className="fas fa-industry me-2"),
                        "State-wise Customer Analytics"
                    ], href="/", className="fs-4")
                ]),
                dbc.Col([
                    dbc.Input(
                        type="search",
                        placeholder="Search customer...",
                        id="search-input",
                        className="form-control bg-dark text-light"
                    )
                ], width=4),
                dbc.Col([
                    dbc.Button(
                        [
                            html.I(className="fas fa-download me-2"),
                            "Export Data"
                        ],
                        id="export-button",
                        color="primary",
                        className="ms-2"
                    )
                ], width="auto")
            ], className="w-100")
        ]),
        color="dark",
        dark=True,
        className="mb-4 shadow-sm"
    )

# Main page component
def create_main_page():
    if df.empty:
        return html.Div("No data available")
    
    # Calculate overall statistics
    total_customers = len(df)
    total_volume = df['Order vol / month'].sum()
    avg_volume = df['Order vol / month'].mean()
    p1_customers = len(df[df['Priority'] == 'P1'])
    
    return dbc.Container([
        # Welcome section
        dbc.Row([
            dbc.Col([
                html.H1("Welcome to Customer Analytics Dashboard", className="text-center mb-4 text-light"),
                html.P("Select a state to view detailed analytics and insights", className="text-center text-muted mb-5")
            ])
        ]),
        
        # Statistics cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-users fa-2x text-primary mb-3"),
                            html.H3(f"{total_customers:,}", className="text-primary"),
                            html.P("Total Customers", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-star fa-2x text-success mb-3"),
                            html.H3(f"{p1_customers:,}", className="text-success"),
                            html.P("P1 Customers", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-chart-line fa-2x text-info mb-3"),
                            html.H3(f"{avg_volume:.1f}", className="text-info"),
                            html.P("Avg Volume/Month", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-box fa-2x text-warning mb-3"),
                            html.H3(f"{total_volume:,.0f}", className="text-warning"),
                            html.P("Total Volume", className="text-muted")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3)
        ], className="mb-5"),
        
        # State selection grid
        dbc.Row([
            dbc.Col([
                html.H2("Select a State", className="text-center mb-4 text-light")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button(
                            [
                                html.I(className="fas fa-map-marker-alt me-2"),
                                state
                            ],
                            href=f"/state/{state}",
                            color="primary",
                            size="lg",
                            className="w-100",
                            style={'height': '60px', 'fontSize': '18px'}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], width=6, lg=4) for state in states
        ])
    ], fluid=True)

# State page component
def create_state_page(state_name):
    if state_name not in state_districts:
        return html.Div("State not found")
    
    districts = state_districts[state_name]
    state_data = df[df['State'] == state_name]
    
    # Calculate state-level metrics
    total_customers = len(state_data)
    p1_customers = len(state_data[state_data['Priority'] == 'P1'])
    avg_volume = state_data['Order vol / month'].mean()
    total_volume = state_data['Order vol / month'].sum()
    
    # Create state-level visualizations
    priority_dist = state_data['Priority'].value_counts()
    fig_priority = px.pie(
        values=priority_dist.values,
        names=priority_dist.index,
        title="Priority Distribution",
        color=priority_dist.index,
        color_discrete_map=priority_colors
    )
    fig_priority.update_layout(
        height=400,
        template="plotly_dark",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Volume trend by district
    district_volumes = state_data.groupby('District Name')['Order vol / month'].mean().sort_values(ascending=False)
    fig_district_volume = px.bar(
        x=district_volumes.index,
        y=district_volumes.values,
        title="Average Volume by District",
        labels={'x': 'District', 'y': 'Average Volume'},
        color=district_volumes.values,
        color_continuous_scale='Viridis'
    )
    fig_district_volume.update_layout(
        height=400,
        template="plotly_dark",
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return dbc.Container([
        # Header with breadcrumb
        dbc.Row([
            dbc.Col([
                html.H2(f"{state_name} Analytics", className="mb-3 text-light"),
                dbc.Breadcrumb(
                    items=[
                        {"label": "Home", "href": "/"},
                        {"label": state_name, "active": True}
                    ],
                    className="mb-4"
                )
            ])
        ]),
        
        # State overview cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-users fa-2x text-primary mb-3"),
                            html.H4(f"{total_customers:,}", className="text-primary"),
                            html.P("Total Customers", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-star fa-2x text-success mb-3"),
                            html.H4(f"{p1_customers:,}", className="text-success"),
                            html.P("P1 Customers", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-chart-line fa-2x text-info mb-3"),
                            html.H4(f"{avg_volume:.1f}", className="text-info"),
                            html.P("Avg Volume/Month", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-box fa-2x text-warning mb-3"),
                            html.H4(f"{total_volume:,.0f}", className="text-warning"),
                            html.P("Total Volume", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3)
        ], className="mb-4"),
        
        # Charts
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_priority)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_district_volume)
            ], width=6)
        ], className="mb-4"),
        
        # District selection
        dbc.Row([
            dbc.Col([
                html.H3("Select a District", className="mb-4 text-light")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button(
                            [
                                html.I(className="fas fa-map-marker-alt me-2"),
                                district
                            ],
                            href=f"/analytics/{state_name}/{district}",
                            color="primary",
                            size="md",
                            className="w-100",
                            style={'height': '50px'}
                        )
                    ])
                ], className="shadow-sm mb-3")
            ], width=6, lg=4) for district in districts
        ])
    ], fluid=True)

# Analytics page component
def create_analytics_page(state_name, district_name):
    district_data = df[(df['State'] == state_name) & (df['District Name'] == district_name)]
    
    if district_data.empty:
        return html.Div("No data found for this district")
    
    # Calculate metrics
    total_customers = len(district_data)
    priority_counts = district_data['Priority'].value_counts()
    avg_volume = district_data['Order vol / month'].mean()
    total_volume = district_data['Order vol / month'].sum()
    
    # Create visualizations
    fig_priority = px.pie(
        values=priority_counts.values,
        names=priority_counts.index,
        title="Priority Distribution",
        color=priority_counts.index,
        color_discrete_map=priority_colors
    )
    fig_priority.update_layout(
        height=400,
        template="plotly_dark",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig_volume = px.box(
        district_data,
        x='Priority',
        y='Order vol / month',
        color='Priority',
        title="Order Volume by Priority",
        color_discrete_map=priority_colors
    )
    fig_volume.update_layout(
        height=400,
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig_scatter = px.scatter(
        district_data,
        x='Order # / month',
        y='Order vol / month',
        color='Priority',
        size='Order month #',
        title="Order Frequency vs Volume",
        color_discrete_map=priority_colors,
        hover_data=['Company GSTIN', 'Order month #'],
        labels={
            'Order # / month': 'Orders per Month',
            'Order vol / month': 'Volume per Month',
            'Order month #': 'Months Active'
        }
    )
    fig_scatter.update_layout(
        height=400,
        template="plotly_dark",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return dbc.Container([
        # Header with breadcrumb
        dbc.Row([
            dbc.Col([
                html.H2(f"{district_name}, {state_name} - Analytics", className="mb-3 text-light"),
                dbc.Breadcrumb(
                    items=[
                        {"label": "Home", "href": "/"},
                        {"label": state_name, "href": f"/state/{state_name}"},
                        {"label": district_name, "active": True}
                    ],
                    className="mb-4"
                )
            ])
        ]),
        
        # KPI Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-users fa-2x text-primary mb-3"),
                            html.H4(f"{total_customers:,}", className="text-primary"),
                            html.P("Total Customers", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-star fa-2x text-success mb-3"),
                            html.H4(f"{priority_counts.get('P1', 0):,}", className="text-success"),
                            html.P("P1 Customers", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-chart-line fa-2x text-info mb-3"),
                            html.H4(f"{avg_volume:.1f}", className="text-info"),
                            html.P("Avg Volume/Month", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-box fa-2x text-warning mb-3"),
                            html.H4(f"{total_volume:,.0f}", className="text-warning"),
                            html.P("Total Volume", className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="shadow-sm h-100")
            ], width=3)
        ], className="mb-4"),
        
        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_priority)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_volume)
            ], width=6)
        ], className="mb-4"),
        
        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_scatter)
            ], width=12)
        ], className="mb-4"),
        
        # Customer Table
        dbc.Row([
            dbc.Col([
                html.H4("Customer Details", className="mb-3 text-light"),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Table.from_dataframe(
                            district_data[['Company GSTIN', 'Priority', 'Order vol / month', 'Order # / month']].head(10),
                            striped=True,
                            bordered=True,
                            hover=True,
                            size='sm',
                            className="table-hover"
                        )
                    ])
                ], className="shadow-sm")
            ])
        ])
    ], fluid=True)

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    create_navbar(),
    html.Div(id='page-content')
])

# Callback for page routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname is None:
        return create_main_page()
    elif pathname.startswith('/state/'):
        state_name = pathname.split('/')[-1]
        return create_state_page(state_name)
    elif pathname.startswith('/analytics/'):
        parts = pathname.split('/')
        if len(parts) >= 4:
            state_name = parts[2]
            district_name = parts[3]
            return create_analytics_page(state_name, district_name)
    
    return html.Div("404 - Page not found")

# Callback for search functionality
@app.callback(
    Output('page-content', 'children', allow_duplicate=True),
    Input('search-input', 'value'),
    prevent_initial_call=True
)
def search_customers(search_term):
    if not search_term:
        raise PreventUpdate
    
    # Search in the dataframe
    search_results = df[
        df['Company GSTIN'].str.contains(search_term, case=False, na=False) |
        df['State'].str.contains(search_term, case=False, na=False) |
        df['District Name'].str.contains(search_term, case=False, na=False)
    ]
    
    if search_results.empty:
        return html.Div("No results found")
    
    # Create a results page
    return dbc.Container([
        html.H2("Search Results", className="mb-4 text-light"),
        dbc.Table.from_dataframe(
            search_results[['Company GSTIN', 'State', 'District Name', 'Priority', 'Order vol / month']].head(20),
            striped=True,
            bordered=True,
            hover=True,
            size='sm'
        )
    ])

if __name__ == '__main__':
    app.run(debug=True)
