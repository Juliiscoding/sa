import streamlit as st
import pandas as pd

# CSS für zentriertes Layout und responsives Design
st.markdown(
    """
    <style>
    /* Gesamte Seite zentrieren */
    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 100vh;
    }

    /* Logo anpassen */
    .logo-container img {
        max-width: 50%; /* Passt das Logo an die Fenstergröße an */
        height: auto;
        margin-bottom: 20px;
    }

    /* Anmeldemaske zentriert unterhalb des Logos */
    .login-container {
        text-align: center;
        width: 100%;
        max-width: 400px; /* Maximale Breite der Anmeldemaske */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Dummy-Benutzerdaten
USER_CREDENTIALS = {
    "admin": "1234",
    "user1": "password1"
}

# Funktion zur Überprüfung der Anmeldedaten
def check_login(username, password):
    return USER_CREDENTIALS.get(username) == password

# Anmeldestatus in Session State speichern
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Logo anzeigen
    st.markdown(
        """
        <div class="logo-container">
            <img src="images/your_logo.png" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Anmeldemaske
    st.markdown(
        """
        <div class="login-container">
            <h2>You´re all in ONE Retail AI - Solution aus dem Hause Hyperion</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    login_button = st.button("Anmelden")

    if login_button:
        if check_login(username, password):
            st.session_state.authenticated = True
            st.success(f"Willkommen, {username}!")
        else:
            st.error("Ungültige Anmeldedaten. Bitte erneut versuchen.")
else:
    # Hauptinhalt der App (Dashboard)
    st.title("KPI-Dashboard für Limitplanung")

    # Hochladen einer Excel-Datei
    uploaded_file = st.file_uploader("Laden Sie eine Excel-Datei hoch", type=["xlsx"])
    if uploaded_file:
        sheet_name = st.sidebar.text_input("Sheet-Name eingeben", "Limit")
        data = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=1)
        st.write("Hochgeladene Daten:")
        st.dataframe(data)

        # Beispiel für KPI-Berechnungen
        data["Deckungsbeitrag"] = data["Plan_Umsatz_VK"] - data["Plan_Umsatz_EK"]
        st.write("Berechnete KPIs:")
        st.dataframe(data)
