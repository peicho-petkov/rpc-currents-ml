#Authors: Elton Shumka, Peicho Petkov

import dash_bootstrap_components as dbc

def Navbar():
    navbar = dbc.NavbarSimple(
            children = [
                dbc.NavItem(dbc.NavLink("Plot Predictions", href="/plot_predictions")),
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
                dbc.NavItem(dbc.NavLink("Manage Model Configurations", href="/manage_configurations")),
                dbc.NavItem(dbc.NavLink("Train Your Models", href="/train")),
                dbc.NavItem(dbc.NavLink("Make Predictions", href="/predict"))
                ],
            brand="Home",
            brand_href="/home",
            sticky="top",
            )
    return navbar
