import dash
from dash import dcc, html, Input, Output, State, MATCH
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dash import no_update
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from themes import forest_theme, rainbow_theme, pastel_theme, sunset_theme, trippy_theme, checker_theme, galaxy_theme, create_poster
import random
import webbrowser
from flask import session, request, redirect
import os
import glob
from uuid import uuid4
import atexit

# Retrieve the secret key from the environment variable
secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise ValueError("No SECRET_KEY set for the app. Please set the SECRET_KEY environment variable.")

# Initialize Dash app
external_stylesheets = [dbc.themes.QUARTZ, dbc.icons.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.server.secret_key = secret_key

server = app.server  # Access Flask server directly

# Set Spotify credentials
cid = os.getenv("SPOTIPY_CLIENT_ID")
secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

# Set up Spotipy OAuth object
sp_oauth = SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope='user-top-read', show_dialog=True)

# Generate unique session ID
def generate_id():
    return str(uuid4())

session_id = generate_id()

# App Layout
app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H4([
                html.I(className="bi bi-file-music-fill"),
                "MyMusicFest"
            ], style={
                "font-family": "helvetica",
                "font-size": "30px",
                "text-align": "left",
                "font-weight": 'light'
            })
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H1("The music festival of the decade.", style={"text-align": "center", "font-size": "60px", "font-style": "italic"}),
        html.H4("And the lineup? All of your favorite artists.", style={"font-family": "helvetica", "font-weight": "lighter", "text-align": "center"}),
        html.Br(),
        html.P(id='login_error_message', style={"text-align": "center"}),
        html.Div([
            html.A(
                dbc.Button(
                    "SEE YOUR FESTIVAL",
                    id="launch-button",
                    style={"font-family": "Gill Sans", "font-weight": "lighter", "letter-spacing": ".1rem"}
                ),
                href=sp_oauth.get_authorize_url(),
                target="_blank"  # Open the link in a new tab
            ),
            html.Br(),
            html.A("Click here if the pop-up doesn't open", href=sp_oauth.get_authorize_url(), target="_blank"),
            dbc.Spinner(html.Div(id="loading-output")),
            html.Br()
        ], style={"text-align": "center"}),
    html.Div(id="poster", children=[], className="mt-4")
])
])

# Helper: Create dynamic poster HTML container
def make_dynamic_poster_container(n_clicks, confirmation_message, username, session_id):
    return dbc.Col([
        html.H4(confirmation_message, style={"text-align": "center", "font-family": "helvetica", "font-weight": "lighter", "letter-spacing": ".1rem"}),
        html.Br(),
        html.Div(html.Img(src=f"assets/poster_{username}_{session_id}_{n_clicks}.png"), style={"height": "100%", "text-align": "center"}),
        html.Br(),
        html.Div(dbc.Button("Log Out", id={"type": "dynamic-delete", "index": n_clicks}, n_clicks=0, color="secondary", style={"font-family": "Gill Sans", "font-weight": "lighter", "letter-spacing": ".1rem"}), style={"text-align": "center", 'width': '100%'}),
        html.Div(style={"height": "50px"})
    ], style={"width": '100%', "display": "inline-block"}, className="m-1", id={"type": "dynamic-card", "index": n_clicks}, width=12)

# Helper: Get top artists for user
def get_top_artists(spotify_user):
    top_artist_dict = spotify_user.current_user_top_artists()
    return [artist['name'] for artist in top_artist_dict['items']]

# Helper: Spotify login (check for existing token)
def spotify_login():
    token_info = session.get("token_info", None)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        return sp
    return None

# Callback: Create festival poster
@app.callback(
    [Output('poster', 'children'), Output('login_error_message', 'children')],
    [Input("launch-button", "n_clicks")],
    [State('poster', 'children')]
)
def on_click(n_clicks, poster_children):
    if n_clicks is not None:
        spotify_user = spotify_login()
        if spotify_user is None:
            return [html.Div(), "Oops... Something went wrong. Refresh the page and try again!"]
        
        try:
            user_info = spotify_user.current_user()
            username = user_info['id']
        except Exception:
            os.remove('.cache')
            return [[], "Oops.. We couldn't load your Spotify credentials. Please try again."]

        # Clean up old posters
        for filename in glob.glob(f"assets/poster_{username}*"):
            os.remove(filename)

        # Generate new poster
        artist_names = [x.upper() for x in get_top_artists(spotify_user)]
        chosen_theme = random.choice([forest_theme, pastel_theme, sunset_theme, trippy_theme, rainbow_theme, checker_theme, galaxy_theme])
        create_poster(chosen_theme, chosen_theme['theme_id'], artist_names, f'{username.upper()}FEST', username, n_clicks, session_id)

        # Confirmation message
        confirm_message = f"Okay {username}! You've got some great taste. Check out your festival below:"
        poster_html_element = make_dynamic_poster_container(n_clicks, confirm_message, username, session_id)
        return [poster_html_element, ""]
    
    return no_update

# Callback: Dynamic logout button
@app.callback(
    Output({"type": "dynamic-card", "index": MATCH}, "style"),
    Input({"type": "dynamic-delete", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def remove_card(_):
    open_url('https://accounts.spotify.com/en/logout')
    os.remove('.cache')
    return {"display": "none"}

# Helper: Open URL
def open_url(url):
    webbrowser.open(url)

# Cleanup function for session-based files
@atexit.register
def cleanup_files():
    try:
        for file in glob.glob(f"assets/*_{session_id}_*.png"):
            os.remove(file)
    except Exception as e:
        print(f"Error cleaning up poster folder: {e}")

# Flask route to handle Spotify OAuth callback
@server.route("/callback")
def callback():
    code = request.args.get("code")
    
    if not code:
        return "Error: No code found in the URL."

    # Exchange code for token
    token_info = sp_oauth.get_access_token(code)
    if not token_info:
        return "Error: Failed to retrieve access token."

    # Store token info in session
    session["token_info"] = token_info

    # JavaScript to close the pop-up window
    return '''
        <script type="text/javascript">
            window.close();
            window.opener.location.reload();  // Reload the opener tab
        </script>
        '''

# Run app
if __name__ == '__main__':
    app.run_server()
