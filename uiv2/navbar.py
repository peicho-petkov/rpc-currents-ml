#Authors: Elton Shumka, Peicho Petkov

import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
            children = [
                dbc.NavItem(dbc.NavLink("Plot Predictions", href="/plot_predictions"), style={'border':'2px solid white', 'background-color': 'cornsilk'}),
#                dbc.DropdownMenu(
#                    nav=True,
#                    in_navbar=True,
#                    label="Menu",
#                    children=[
#                        dbc.DropdownMenuItem('Manage Model Configurations'),
#                        dbc.DropdownMenuItem('Train Your Models'),
#                        dbc.DropdownMenuItem('Make Predictions')
#                        ],
#                    ),
                dbc.NavItem(dbc.NavLink("Manage Model Configurations", href="/manage_configurations"), style={'border': '2px solid white', 'background-color': 'cornsilk'}),
                dbc.NavItem(dbc.NavLink("Train Models", href="/train"), style={'border': '2px solid white', 'background-color': 'cornsilk'}),
                dbc.NavItem(dbc.NavLink("Make Predictions", href="/predict"), style={'border': '2px solid white', 'background-color': 'cornsilk'}),
                dbc.NavItem(dbc.NavLink("Warnings and Errors", href="/warnings"), style={'border': '2px solid white', 'background-color': 'cornsilk'}),
                dbc.NavItem(dbc.NavLink("About", href="/about"), style={'border': '2px solid white', 'background-color': 'cornsilk'}),
                ],
            brand="Home",
            brand_href="/home",
            sticky="top",
            style={'background-color':'blue', 'color':'cornsilk'}
            #pills=True
            )
    return navbar
