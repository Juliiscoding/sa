import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel der App
st.title("KPI-Dashboard für Limitplanung")

# Daten hochladen
st.sidebar.header("Daten hochladen")
uploaded_file = st.sidebar.file_uploader("Laden Sie eine Excel-Datei hoch", type=["xlsx"])

if uploaded_file:
    # Excel-Daten laden
    sheet_name = st.sidebar.text_input("Sheet-Name eingeben", "Limit")
    data = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=3)

    # KPI-Berechnungen
    data["Deckungsbeitrag"] = data["Plan_Umsatz_VK"] - data["Plan_Umsatz_EK"]
    data["Lagerumschlagsgeschwindigkeit"] = data["Plan_Umsatz_EK"] / (data["Limit_Verfügbar"] * 0.5)

    # KPIs anzeigen
    st.header("KPIs")
    st.metric("Durchschnittlicher Deckungsbeitrag", f"{data['Deckungsbeitrag'].mean():,.2f} €")
    st.metric(
        "Durchschnittliche Lagerumschlagsgeschwindigkeit",
        f"{data['Lagerumschlagsgeschwindigkeit'].mean():.2f}",
    )

    # Kategorien filtern
    category = st.selectbox("Kategorie auswählen", data["Description"].dropna().unique())
    filtered_data = data[data["Description"] == category]

    # Diagramm: Lagerumschlagsgeschwindigkeit
    st.subheader("Lagerumschlagsgeschwindigkeit pro Kategorie")
    fig, ax = plt.subplots()
    ax.bar(data["Description"], data["Lagerumschlagsgeschwindigkeit"], color="skyblue")
    ax.set_title("Lagerumschlagsgeschwindigkeit")
    ax.set_xlabel("Kategorie")
    ax.set_ylabel("LUG")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # Tabelle anzeigen
    st.subheader(f"Daten für Kategorie: {category}")
    st.write(filtered_data)
else:
    st.info("Laden Sie eine Excel-Datei hoch, um zu starten.")
