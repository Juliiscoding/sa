import streamlit as st
import pandas as pd

# Logo anzeigen
st.image("images/logo.png", width=200)  # Stelle sicher, dass "logo.png" im Ordner "images" ist.

# Dummy-Benutzerdaten
USER_CREDENTIALS = {
    "admin": "1234",
    "user1": "password1"
}

# Funktion zur Überprüfung der Anmeldedaten
def check_login(username, password):
    return USER_CREDENTIALS.get(username) == password

# Anmeldemaske
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Willkommen bei deinem SaaS AI-Dashboard")
    st.subheader("Login")
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
