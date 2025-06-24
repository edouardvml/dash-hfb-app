import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from pathlib import Path


# ── 1) Charger les données en chemin relatif propre ────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / ".data" / "input_B2B_purchase_V2.csv"
df = pd.read_csv(DATA_FILE, delimiter=",")

#df = pd.read_csv(resource_path(r".data/input_B2B_purchase_V2.csv"), delimiter=",")  # Assurez-vous que df_2 est chargé si nécessaire
df["date_purchase_month"] = pd.to_datetime(df["date_purchase_month"], format="%Y-%m-%d")
df["hfb_no"] = df["hfb_no"].astype(str)  # Assurez-vous que hfb_no est de type str


#print(df.hfb_no.unique())
#print(df.dtypes)
#print(df.head())

# --- 2. Initialiser l'app ---
app = Dash(__name__)
server = app.server  # <= indispensable pour Gunicorn
app.title = "Évolution achats par secteur et HFB"

# --- 3. Layout ---
app.layout = html.Div([
    html.H2("Évolution des acheteurs par HFB et secteur"),
    html.Label("Sélectionne un secteur :"),
    dcc.Dropdown(
        id='industry-dropdown',
        options=[{'label': seg, 'value': seg} for seg in sorted(df['industry_segment_label'].unique())],
        value=sorted(df['industry_segment_label'].unique())[0],
        clearable=False
    ),
    html.Label("Filtre HFB (multi‑séléction) :"),
    dcc.Dropdown(id='hfb-dropdown', multi=True),
    dcc.Graph(id='evolution-graph')
])

# --- 4. Callback : rafraîchir les options HFB selon le secteur ---
@app.callback(
    Output('hfb-dropdown', 'options'),
    Output('hfb-dropdown', 'value'),
    Input('industry-dropdown', 'value')
)
def update_hfb_options(selected_segment):
    hfb_opts = df[df['industry_segment_label'] == selected_segment]['hfb_no'].unique()
    options = [{'label': f"HFB {h}", 'value': h} for h in sorted(hfb_opts)]
    return options, []  # pas de sélection par défaut

# --- 5. Callback : construire le graphique ---
@app.callback(
    Output('evolution-graph', 'figure'),
    Input('industry-dropdown', 'value'),
    Input('hfb-dropdown', 'value')
)
def update_graph(selected_segment, selected_hfbs):
    dff = df[df['industry_segment_label'] == selected_segment]
    if selected_hfbs:
        dff = dff[dff['hfb_no'].isin(selected_hfbs)]
    fig = px.line(dff, x='date_purchase_month', y='cust_by_hfb', color='hfb_no',
                  title=f"Évolution – Secteur : {selected_segment}",
                  markers=True)
    fig.update_layout(xaxis_title="Mois", yaxis_title="Nb d'acheteurs", legend_title="HFB")
    return fig

# --- 6. Lancer le serveur avec la nouvelle méthode ---
if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0", port=8050, debug=False)
