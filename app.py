import streamlit as st
import pandas as pd
from streamlit_gps_location import gps_location_button
from fpdf import FPDF
import tempfile
from datetime import date


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Field Report App",
    layout="centered"
)

st.title("📍 Field Report App")
st.write("Mobile-style app to document a scientific discovery with notes, GPS location, photo evidence, and a PDF report.")


# -----------------------------
# Function to create the PDF
# -----------------------------
def create_pdf(researcher, title, notes, latitude, longitude, photo_file):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_fill_color(126, 87, 194)  # purple
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 18, "FIELD REPORT", ln=True, align="C", fill=True)

    pdf.ln(10)

    # Report information
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 8, "Researcher:", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, researcher, ln=True)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 8, "Date:", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, str(date.today()), ln=True)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 8, "Coordinates:", 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"{latitude}, {longitude}", ln=True)

    pdf.ln(6)

    # Discovery title
    pdf.set_font("Arial", "B", 13)
    pdf.multi_cell(0, 8, f"Discovery: {title}")

    pdf.ln(2)

    # Notes
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "Observation Notes:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, notes)

    pdf.ln(6)

    # Photo
    if photo_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            temp_image.write(photo_file.getvalue())
            image_path = temp_image.name

        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, "Visual Evidence:", ln=True)

        # Add image with safe size
        pdf.image(image_path, x=30, w=150)

    # Return PDF as bytes
    return pdf.output(dest="S").encode("latin-1")


# -----------------------------
# 1. User information
# -----------------------------
st.header("1. User Information")

researcher = st.text_input("Researcher name")
discovery_title = st.text_input("Title of the discovery")
notes = st.text_area("Description / notes", height=120)


# -----------------------------
# 2. GPS location
# -----------------------------
st.header("2. GPS Location")

location_data = gps_location_button(buttonText="Get my location")

latitude = None
longitude = None

if location_data is not None:
    latitude = location_data.get("latitude")
    longitude = location_data.get("longitude")

    if latitude is not None and longitude is not None:
        st.success("Location captured successfully.")
        st.write(f"Latitude: {latitude}")
        st.write(f"Longitude: {longitude}")

        map_data = pd.DataFrame({
            "lat": [latitude],
            "lon": [longitude]
        })

        st.map(map_data)
    else:
        st.warning("Location data was received, but latitude or longitude is missing.")
else:
    st.info("Press the button to capture your GPS location.")


# -----------------------------
# 3. Visual evidence
# -----------------------------
st.header("3. Visual Evidence")

photo = st.camera_input("Take a photo as evidence")

if photo is not None:
    st.image(photo, caption="Captured evidence", use_container_width=True)


# -----------------------------
# 4. PDF report generation
# -----------------------------
st.header("4. Generate PDF Report")

missing_fields = []

if not researcher:
    missing_fields.append("researcher name")
if not discovery_title:
    missing_fields.append("discovery title")
if not notes:
    missing_fields.append("description / notes")
if latitude is None or longitude is None:
    missing_fields.append("GPS location")
if photo is None:
    missing_fields.append("photo evidence")

if missing_fields:
    st.warning("Complete the following fields before generating the report: " + ", ".join(missing_fields))
else:
    try:
        pdf_bytes = create_pdf(
            researcher,
            discovery_title,
            notes,
            latitude,
            longitude,
            photo
        )

        st.success("Report generated successfully.")

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="field_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as e:
        st.error("Something went wrong while creating the PDF report.")
        st.write(e)
