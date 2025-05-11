# import streamlit as st
# import pandas as pd
# import numpy as np
# from xgboost import XGBClassifier
# from sklearn.preprocessing import LabelEncoder
# import requests
# import json
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# from fpdf import FPDF
# from datetime import datetime

# # Enhanced medical knowledge base with more pediatric symptoms and refined weights
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio",
#              "options": ["<100.4°F", "100.4-102.2°F", "102.2-104°F", ">104°F"],
#              "weights": {"<100.4°F": 1, "100.4-102.2°F": 2, "102.2-104°F": 3, ">104°F": 3}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 1, "1-3 days": 2, "3-7 days": 3, ">7 days": 3}}
#         ],
#         "red_flags": ["Fever >100.4°F in infants <3 months", "Fever >104°F"]
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping"],
#              "weights": {"Dry": 1, "Productive": 2, "Barking": 3, "Whooping": 3}},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1, "Nighttime": 2, "With feeding": 2, "After exercise": 2, "All day": 3}}
#         ],
#         "red_flags": ["Whooping sound on inspiration", "Cough causing vomiting"]
#     },
#     "RUNNY_NOSE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Nasal discharge with foul odor"]
#     },
#     "SNEEZING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["Occasional", "Frequent", "Constant"],
#              "weights": {"Occasional": 1, "Frequent": 2, "Constant": 3}}
#         ],
#         "red_flags": []
#     },
#     "MUSCLE_ACHES": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Severe muscle pain with fever"]
#     },
#     "HEADACHE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Severe headache with fever", "Headache with neck stiffness"]
#     },
#     "WHEEZING": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Wheezing in infants <6 months"]
#     },
#     "RESPIRATORY_DISTRESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["None", "Mild (intercostal retractions)", "Moderate (nasal flaring)", "Severe (grunting, head bobbing)"],
#              "weights": {"None": 0, "Mild (intercostal retractions)": 2, "Moderate (nasal flaring)": 3, "Severe (grunting, head bobbing)": 3}}
#         ],
#         "red_flags": ["Severe respiratory distress", "Grunting in infants"]
#     },
#     "VOMITING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["1-2 times/day", "3-5 times/day", ">5 times/day"],
#              "weights": {"1-2 times/day": 1, "3-5 times/day": 2, ">5 times/day": 3}}
#         ],
#         "red_flags": ["Vomiting with bile", "Projectile vomiting"]
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1, "5-8 loose stools/day": 2, ">8 loose stools/day": 3, "Watery": 3}},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1, "Mucoid": 2, "Bloody": 3, "Rice-water": 3}}
#         ],
#         "red_flags": ["Bloody diarrhea", "Dehydration signs"]
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1, "No tears": 2, "Sunken eyes": 3, "Decreased urine output": 3, "Lethargy": 3}}
#         ],
#         "red_flags": ["Severe dehydration signs"]
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3, "Doubled over": 3}}
#         ],
#         "red_flags": ["Right lower quadrant pain", "Pain with vomiting"]
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Macular", "Papular", "Vesicular", "Petechial/Purpuric"],
#              "weights": {"Macular": 1, "Papular": 2, "Vesicular": 3, "Petechial/Purpuric": 3}}
#         ],
#         "red_flags": ["Petechial rash with fever"]
#     },
#     "NECK_STIFFNESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Neck stiffness with fever", "Opisthotonus"]
#     },
#     "PHOTOPHOBIA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild light sensitivity", "Moderate (avoids light)", "Severe (eyes tightly closed)"],
#              "weights": {"Mild light sensitivity": 1, "Moderate (avoids light)": 2, "Severe (eyes tightly closed)": 3}}
#         ],
#         "red_flags": ["Photophobia with headache", "Photophobia with neck stiffness"]
#     }
# }

# @st.cache_data
# def load_data(file_path):
#     """Load the dataset from a CSV file."""
#     df = pd.read_csv(file_path)
#     # Fill NaN values with 0 for all symptoms
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# def calculate_age_risk_factor(age):
#     """Calculate risk factor based on age (higher risk for infants and immunocompromised)."""
#     if age < 3: return 1.5  # Higher weight for infants
#     elif age < 12: return 1.2  # Moderate weight for young children
#     else: return 1.0  # Standard weight for older children

# def apply_clinical_overrides(prediction, symptoms, age):
#     """Apply clinical rules to override model predictions when specific patterns are detected."""
#     # Meningitis override
#     if "NECK_STIFFNESS" in symptoms and "FEVER" in symptoms and "PHOTOPHOBIA" in symptoms and age < 5:
#         return "Meningitis (clinical override)", 0.95
#     # Pertussis pattern
#     if "COUGH_PAROXYSMAL" in symptoms and "COUGH_POST_TUSSIVE" in symptoms:
#         return "Pertussis (clinical override)", 0.9
#     # Kawasaki criteria
#     if "FEVER" in symptoms and "STRAWBERRY_TONGUE" in symptoms and "RASH" in symptoms and age < 5:
#         return "Kawasaki Disease (clinical override)", 0.85
#     # Scarlet fever
#     if "STRAWBERRY_TONGUE" in symptoms and "SORE_THROAT" in symptoms and "RASH" in symptoms:
#         return "Scarlet Fever (clinical override)", 0.85
#     # Measles
#     if "KOPLIK_SPOTS" in symptoms and "FEVER" in symptoms and "RASH" in symptoms:
#         return "Measles (clinical override)", 0.9
#     return prediction, None

# def find_nearby_doctors(lat, lon, radius=5000):
#     """
#     Find nearby doctors and pediatricians using Overpass API.
#     Returns a DataFrame with name, address, and coordinates.
#     """
#     overpass_url = "https://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json];
#     (
#       node["amenity"="doctors"](around:{radius},{lat},{lon});
#       node["amenity"="clinic"](around:{radius},{lat},{lon});
#       node["healthcare"="doctor"](around:{radius},{lat},{lon});
#       node["healthcare"="pediatrician"](around:{radius},{lat},{lon}); 
#     );
#     out center;
#     """
#     try:
#         response = requests.get(overpass_url, params={'data': query})
#         response.raise_for_status()
#         data = response.json()
#         doctors = []
#         for element in data['elements']:
#             name = element.get('tags', {}).get('name', 'Unknown')
#             address = element.get('tags', {}).get('addr:full', 
#                       element.get('tags', {}).get('addr:street', 'Address not available'))
#             specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
#             # Get coordinates
#             if 'lat' in element and 'lon' in element:
#                 lat = element['lat']
#                 lon = element['lon']
#             elif 'center' in element:
#                 lat = element['center']['lat']
#                 lon = element['center']['lon']
#             else:
#                 continue
#             doctors.append({
#                 'name': name,
#                 'address': address,
#                 'specialty': specialty,
#                 'latitude': lat,
#                 'longitude': lon
#             })
#         return pd.DataFrame(doctors)
#     except Exception as e:
#         st.error(f"Error fetching nearby doctors: {e}")
#         return pd.DataFrame()

# def show_nearby_doctors():
#     """Show interface for finding nearby doctors."""
#     with st.expander("🚑 Find Nearby Doctors & Pediatricians", expanded=False):
#         st.write("Locate nearby healthcare providers based on your location")
#         # Location input options
#         location_method = st.radio("Select location method:", 
#                                  ["Use my current location", "Enter address manually"])
#         if location_method == "Use my current location":
#             lat = st.number_input("Latitude", value=40.7128, format="%.6f")
#             lon = st.number_input("Longitude", value=-74.0060, format="%.6f")
#         else:
#             address = st.text_input("Enter full address:")
#             if address:
#                 geolocator = Nominatim(user_agent="pediatric_symptom_checker")
#                 try:
#                     location = geolocator.geocode(address)
#                     if location:
#                         lat, lon = location.latitude, location.longitude
#                         st.success(f"Found location: {location.address}")
#                     else:
#                         st.warning("Could not find location. Using default coordinates.")
#                         lat, lon = 40.7128, -74.0060  # Default to NYC
#                 except Exception as e:
#                     st.error(f"Geocoding error: {e}")
#                     lat, lon = 40.7128, -74.0060
#         search_radius = st.slider("Search radius (meters)", 500, 10000, 2000)
#         if st.button("Find Nearby Doctors", key="find_doctors"):
#             with st.spinner("Searching for nearby doctors..."):
#                 doctors_df = find_nearby_doctors(lat, lon, search_radius)
#                 if not doctors_df.empty:
#                     st.success(f"Found {len(doctors_df)} doctors/clinics nearby")
#                     # Create map centered at user's location
#                     m = folium.Map(location=[lat, lon], zoom_start=13)
#                     # Add marker for user's location
#                     folium.Marker(
#                         [lat, lon],
#                         popup="Your Location",
#                         icon=folium.Icon(color="blue", icon="user")
#                     ).add_to(m)
#                     # Add markers for each doctor
#                     for idx, row in doctors_df.iterrows():
#                         popup_text = f"""
#                         <b>{row['name']}</b><br>
#                         <i>{row['specialty']}</i><br>
#                         {row['address']}
#                         """
#                         icon_color = "green" if "pediatric" in row['specialty'].lower() else "red"
#                         folium.Marker(
#                             [row['latitude'], row['longitude']],
#                             popup=popup_text,
#                             icon=folium.Icon(color=icon_color, icon="medkit")
#                         ).add_to(m)
#                     # Display the map
#                     folium_static(m)
#                     # Show the data in a table
#                     st.subheader("Nearby Healthcare Providers")
#                     st.dataframe(doctors_df[['name', 'specialty', 'address']])
#                 else:
#                     st.warning("No doctors found in the specified area. Try increasing the search radius.")

# def create_pdf_report(patient_info, symptoms, prediction, probabilities, red_flags, recommendations):
#     """Create a PDF report of the symptom analysis."""
#     pdf = FPDF()
#     pdf.add_page()
#     # Set font for the title
#     pdf.set_font("Arial", 'B', 16)
#     pdf.cell(0, 10, "Pediatric Symptom Checker Report", ln=True, align='C')
#     pdf.ln(10)
#     # Add date and time
#     pdf.set_font("Arial", '', 10)
#     pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
#     pdf.ln(5)
#     # Patient Information section
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Patient Information", ln=True)
#     pdf.set_font("Arial", '', 12)
#     pdf.cell(0, 10, f"Age: {patient_info['age']} months", ln=True)
#     pdf.cell(0, 10, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", ln=True)
#     pdf.ln(5)
#     # Symptoms section
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Reported Symptoms", ln=True)
#     pdf.set_font("Arial", '', 12)
#     for symptom, details in symptoms.items():
#         pdf.cell(0, 10, f"- {symptom.replace('_', ' ').title()}: Severity {details['value']:.1f} (Weight {details['weight']:.1f})", ln=True)
#     pdf.ln(5)
#     # Diagnosis section
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Diagnosis", ln=True)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, f"Most likely condition: {prediction}", ln=True)
#     pdf.ln(3)
#     pdf.set_font("Arial", '', 12)
#     pdf.cell(0, 10, "Top Possible Conditions:", ln=True)
#     for i, (condition, prob) in enumerate(probabilities.items(), 1):
#         pdf.cell(0, 10, f"{i}. {condition}: {prob:.1%}", ln=True)
#     pdf.ln(5)
#     # Red Flags section
#     if red_flags:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.cell(0, 10, "Red Flags Identified", ln=True)
#         pdf.set_font("Arial", '', 12)
#         for flag in red_flags:
#             pdf.cell(0, 10, f"- {flag}", ln=True)
#         pdf.ln(5)
#     # Recommendations section
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Recommended Actions", ln=True)
#     pdf.set_font("Arial", '', 12)
#     for rec in recommendations:
#         pdf.multi_cell(0, 10, rec)
#     pdf.ln(5)
#     # Disclaimer
#     pdf.set_font("Arial", 'I', 10)
#     pdf.multi_cell(0, 10, "Disclaimer: This report is generated by an AI system and is not a substitute for professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
#     return pdf.output(dest='S').encode('latin1')

# def get_recommendations(prediction, age, medical_history):
#     """Generate recommendations based on the prediction."""
#     recommendations = []
#     if "Meningitis" in prediction:
#         recommendations.append("""
#         EMERGENCY: Seek immediate medical attention
#         - This is a medical emergency requiring IV antibiotics
#         - Go to nearest ER immediately
#         - Do not wait for symptoms to worsen
#         """)
#     elif "Epiglottitis" in prediction:
#         recommendations.append("""
#         EMERGENCY: Do not examine throat
#         - Risk of complete airway obstruction
#         - Keep child calm and upright
#         - Call emergency services immediately
#         """)
#     elif prediction in ["Bronchiolitis", "Pneumonia", "Dehydration"]:
#         recommendations.append("""
#         Urgent: Contact your pediatrician within 4-6 hours
#         - Monitor respiratory rate closely
#         - Keep child hydrated
#         - Watch for signs of worsening distress
#         """)
#     elif prediction in ["Influenza (Flu)", "Strep Throat", "Pertussis"]:
#         recommendations.append("""
#         Contact your pediatrician within 24 hours
#         - Rest and fluids
#         - Monitor fever pattern
#         - Watch for complications
#         - May need specific testing/treatment
#         """)
#     else:
#         recommendations.append("""
#         Monitor at home
#         - Symptomatic treatment as needed
#         - Contact doctor if symptoms worsen or persist >3 days
#         - Ensure adequate hydration
#         - Watch for new symptoms
#         """)
#     # Age-specific recommendations
#     if age < 6:
#         recommendations.append("For infants under 6 months, always consult a doctor for any significant symptoms")
#     if "Immunocompromised" in medical_history:
#         recommendations.append("Immunocompromised children may need earlier evaluation for fever or infection")
#     return recommendations

# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
#     st.title("👶 Pediatric Symptom Checker")

#     # Load data
#     file_path = "10000.csv"  # Replace with your actual file path
#     df = load_data(file_path)

#     # Encode the target variable
#     label_encoder = LabelEncoder()
#     df["CONDITION"] = label_encoder.fit_transform(df["CONDITION"])

#     # Get all available symptoms from dataset
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]

#     # Age input
#     with st.expander("Patient Information", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Age (months)", min_value=0, max_value=216, value=24, step=1)
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                 default=[]
#             )

#     # Step 1: Primary symptom selection
#     with st.expander("Step 1: Select main symptoms", expanded=True):
#         primary_symptoms = st.multiselect(
#             "What symptoms is your child experiencing?",
#             options=all_symptoms,
#             placeholder="Select symptoms..."
#         )

#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("Step 2: Provide symptom details", expanded=True):
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS:
#                     st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
#                     symptom_weight = 1.0  # Base weight
#                     for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                         response = None
#                         if question["type"] == "radio":
#                             response = st.radio(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "selectbox":
#                             response = st.selectbox(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "checkbox":
#                             response = st.multiselect(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         if response:
#                             if isinstance(response, list):  # For checkbox questions
#                                 for item in response:
#                                     symptom_weight *= question["weights"][item]
#                             else:  # For radio/selectbox
#                                 symptom_weight *= question["weights"][response]
#                     symptom_details[symptom] = {
#                         "value": 1.0,  # Base value
#                         "weight": symptom_weight
#                     }
#                     # Show clinical notes if available
#                     if "note" in SYMPTOM_DEFINITIONS[symptom]:
#                         st.info(SYMPTOM_DEFINITIONS[symptom]["note"])
#                 else:
#                     # For symptoms without follow-up questions
#                     severity = st.slider(
#                         f"Severity of {symptom.lower().replace('_', ' ')}",
#                         min_value=0.1,
#                         max_value=3.0,
#                         value=1.0,
#                         step=0.1,
#                         key=symptom
#                     )
#                     symptom_details[symptom] = {
#                         "value": severity,
#                         "weight": 1.0
#                     }

#     # Initialize session state for prediction results
#     if 'prediction_results' not in st.session_state:
#         st.session_state.prediction_results = None

#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return

#         # Prepare features (only numerical columns)
#         numerical_cols = [col for col in df.columns if col != "CONDITION"]
#         X = df[numerical_cols]
#         y = df["CONDITION"]

#         # Train model - using XGBoost for better performance
#         model = XGBClassifier(
#             n_estimators=200,
#             learning_rate=0.1,
#             max_depth=4,
#             subsample=0.8,
#             random_state=42
#         )
#         model.fit(X, y)

#         # Prepare input features
#         input_features = {col: 0.0 for col in numerical_cols}
#         # Apply symptom weights and age factor
#         age_factor = calculate_age_risk_factor(age)
#         for symptom, details in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = details["value"] * details["weight"] * age_factor

#         # Additional weight for concerning medical history
#         if "Immunocompromised" in medical_history:
#             for symptom in input_features:
#                 if input_features[symptom] > 0:
#                     input_features[symptom] *= 1.5

#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])[numerical_cols]

#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]

#         # Decode prediction back to disease name
#         prediction = label_encoder.inverse_transform([prediction])[0]

#         # Apply clinical overrides
#         override_prediction, override_prob = apply_clinical_overrides(prediction, primary_symptoms, age)
#         if override_prediction:
#             prediction = override_prediction

#         # Get top 5 conditions with probabilities
#         prob_df = pd.DataFrame({
#             "Condition": label_encoder.inverse_transform(model.classes_),
#             "Probability": probabilities
#         }).sort_values("Probability", ascending=False).head(5)

#         # Highlight overridden condition if applicable
#         if override_prediction:
#             prob_df.loc[prob_df['Condition'] == override_prediction.split(' (')[0], 'Probability'] = override_prob

#         # Get red flags
#         red_flags = []
#         for symptom in primary_symptoms:
#             if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                 red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])

#         # Age-specific red flags
#         if age < 3 and "FEVER" in primary_symptoms:
#             red_flags.append("Fever in infants <3 months requires immediate evaluation")
#         if age < 6 and "COUGH" in primary_symptoms and "WHEEZING" in primary_symptoms:
#             red_flags.append("Wheezing in infants <6 months may indicate serious illness")
#         if "PETECHIAL/PURPURIC" in primary_symptoms and "FEVER" in primary_symptoms:
#             red_flags.append("Petechial rash with fever may indicate meningococcemia - seek IMMEDIATE care")

#         # Get recommendations
#         recommendations = get_recommendations(prediction, age, medical_history)

#         # Store results in session state
#         st.session_state.prediction_results = {
#             "prediction": prediction,
#             "probabilities": dict(zip(prob_df['Condition'], prob_df['Probability'])),
#             "red_flags": red_flags,
#             "recommendations": recommendations,
#             "patient_info": {
#                 "age": age,
#                 "medical_history": medical_history
#             },
#             "symptoms": symptom_details
#         }

#     # Display results if available
#     if st.session_state.prediction_results:
#         results = st.session_state.prediction_results
#         # Create PDF report
#         pdf_report = create_pdf_report(
#             results['patient_info'],
#             results['symptoms'],
#             results['prediction'],
#             results['probabilities'],
#             results['red_flags'],
#             results['recommendations']
#         )
#         # Add download button at the top right
#         col1, col2 = st.columns([4, 1])
#         with col1:
#             st.success(f"### Most likely condition: **{results['prediction']}**")
#         with col2:
#             st.download_button(
#                 label="📄 Download Report",
#                 data=pdf_report,
#                 file_name=f"pediatric_symptom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
#                 mime="application/pdf",
#                 use_container_width=True
#             )
#         # Display results in two columns
#         col1, col2 = st.columns([1, 2])
#         with col1:
#             # Show probabilities
#             st.subheader("Top Possible Conditions")
#             prob_df = pd.DataFrame({
#                 "Condition": results['probabilities'].keys(),
#                 "Probability": results['probabilities'].values()
#             }).sort_values("Probability", ascending=False)
#             # Format probabilities with colors
#             def color_probs(val):
#                 color = 'red' if val > 0.7 else 'orange' if val > 0.3 else 'green'
#                 return f'color: {color}; font-weight: bold'
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"})
#                       .applymap(color_probs, subset=['Probability']),
#                 hide_index=True
#             )
#         with col2:
#             # Show red flags
#             if results['red_flags']:
#                 st.subheader("⚠️ Red Flags to Watch For")
#                 for flag in results['red_flags']:
#                     st.error(f"• {flag}")
#             else:
#                 st.subheader("ℹ️ No Urgent Red Flags")
#                 st.info("No urgent red flags identified based on current symptoms")
#             # Show recommendations
#             st.subheader("ℹ️ Recommended Actions")
#             for rec in results['recommendations']:
#                 st.warning(rec)

#     # Show the nearby doctors feature (always visible)
#     show_nearby_doctors()

# if __name__ == "__main__":
#     main()




# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.pipeline import Pipeline
# import requests
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# # Add this import at the top with other imports
# from fpdf import FPDF
# import base64
# from datetime import datetime

# # Add this function somewhere before the main() function
# def generate_pdf_report(patient_info, symptoms, prediction, probabilities_df, red_flags, recommendations):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 16)
    
#     # Header
#     pdf.cell(0, 10, "Pediatric Health Report", 0, 1, 'C')
#     pdf.set_font("Arial", '', 12)
#     pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C')
#     pdf.ln(10)
    
#     # Patient Information
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Patient Information", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     pdf.cell(0, 10, f"Age: {patient_info['age']} months", 0, 1)
#     pdf.cell(0, 10, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", 0, 1)
#     pdf.ln(5)
    
#     # Symptoms
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Reported Symptoms", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     for symptom, details in symptoms.items():
#         pdf.cell(0, 10, f"- {symptom.replace('_', ' ').title()}: Severity score {details}", 0, 1)
#     pdf.ln(5)
    
#     # Diagnosis
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Diagnostic Assessment", 0, 1)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(0, 10, f"Most Likely Condition: {prediction}", 0, 1)
#     pdf.set_font("Arial", '', 12)
    
#     # Probability table
#     pdf.cell(0, 10, "Condition Probabilities:", 0, 1)
#     col_width = pdf.w / 3
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(col_width, 10, "Condition", 1)
#     pdf.cell(col_width, 10, "Probability", 1, 1)
#     pdf.set_font("Arial", '', 12)
    
#     for _, row in probabilities_df.iterrows():
#         pdf.cell(col_width, 10, row['Condition'], 1)
#         pdf.cell(col_width, 10, f"{row['Probability']:.2%}", 1, 1)
#     pdf.ln(5)
    
#     # Red Flags
#     if red_flags:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.cell(0, 10, "Red Flags", 0, 1)
#         pdf.set_font("Arial", '', 12)
#         for flag in red_flags:
#             pdf.cell(0, 10, f"- {flag}", 0, 1)
#         pdf.ln(5)
    
#     # Recommendations
#     if recommendations:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.cell(0, 10, "Recommendations", 0, 1)
#         pdf.set_font("Arial", '', 12)
#         for rec in recommendations:
#             pdf.cell(0, 10, f"- {rec}", 0, 1)
#         pdf.ln(5)
    
#     # Disclaimer
#     pdf.set_font("Arial", 'I', 10)
#     pdf.multi_cell(0, 10, "Disclaimer: This report is generated by an AI system and should not replace professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
    
#     return pdf

# # Load and preprocess the dataset
# @st.cache_data
# def load_data(file_path):
#     df = pd.read_csv(file_path)
#     # Fill NaN values with 0 for all symptoms
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# # Enhanced medical knowledge base with more pediatric symptoms and refined weights
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio",
#              "options": ["<100.4°F", "100.4-102.2°F", "102.2-104°F", ">104°F"],
#              "weights": {"<100.4°F": 1, "100.4-102.2°F": 2, "102.2-104°F": 3, ">104°F": 4}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 1, "1-3 days": 2, "3-7 days": 3, ">7 days": 4}}
#         ],
#         "red_flags": ["Fever >100.4°F in infants <3 months", "Fever >104°F"]
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping"],
#              "weights": {"Dry": 1, "Productive": 2, "Barking": 3, "Whooping": 4}},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1, "Nighttime": 2, "With feeding": 2, "After exercise": 2, "All day": 3}}
#         ],
#         "red_flags": ["Whooping sound on inspiration", "Cough causing vomiting"]
#     },
#     "RUNNY_NOSE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Nasal discharge with foul odor"]
#     },
#     "SNEEZING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["Occasional", "Frequent", "Constant"],
#              "weights": {"Occasional": 1, "Frequent": 2, "Constant": 3}}
#         ]
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1, "5-8 loose stools/day": 2, ">8 loose stools/day": 3, "Watery": 3}},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1, "Mucoid": 2, "Bloody": 3, "Rice-water": 3}}
#         ]
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1, "No tears": 2, "Sunken eyes": 3, "Decreased urine output": 3, "Lethargy": 4}}
#         ],
#         "red_flags": ["Severe dehydration signs"]
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3, "Doubled over": 4}}
#         ]
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Macular", "Papular", "Vesicular", "Petechial/Purpuric"],
#              "weights": {"Macular": 1, "Papular": 2, "Vesicular": 3, "Petechial/Purpuric": 4}}
#         ]
#     },
#     "HEADACHE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Severe headache with fever", "Headache with neck stiffness"]
#     }
# }

# # Find nearby doctors using Overpass API
# def find_nearby_doctors(lat, lon, radius=5000):
#     overpass_url = "https://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json];
#     (
#         node["amenity"="doctors"](around:{radius},{lat},{lon});
#         node["amenity"="clinic"](around:{radius},{lat},{lon});
#         node["healthcare"="doctor"](around:{radius},{lat},{lon});
#         node["healthcare"="pediatrician"](around:{radius},{lat},{lon});
#     );
#     out center;
#     """
#     try:
#         response = requests.get(overpass_url, params={'data': query})
#         response.raise_for_status()
#         data = response.json()
#         doctors = []
#         for element in data['elements']:
#             name = element.get('tags', {}).get('name', 'Unknown')
#             address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Address not available'))
#             specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
#             lat = element.get('lat', element.get('center', {}).get('lat'))
#             lon = element.get('lon', element.get('center', {}).get('lon'))
#             if lat and lon:
#                 doctors.append({'name': name, 'address': address, 'specialty': specialty, 'latitude': lat, 'longitude': lon})
#         return pd.DataFrame(doctors)
#     except Exception as e:
#         st.error(f"Error fetching nearby doctors: {e}")
#         return pd.DataFrame()

# # Show nearby doctors interface
# def show_nearby_doctors():
#     with st.expander("🚑 Find Nearby Doctors & Pediatricians", expanded=False):
#         st.write("Locate nearby healthcare providers based on your location")
#         location_method = st.radio("Select location method:", ["Use my current location", "Enter address manually"])
#         if location_method == "Use my current location":
#             try:
#                 loc = st.experimental_get_query_params().get("location", None)
#                 if loc:
#                     lat, lon = map(float, loc[0].split(","))
#                 else:
#                     lat, lon = 40.7128, -74.0060  # Default to NYC
#             except Exception as e:
#                 st.error(f"Geocoding error: {e}")
#                 lat, lon = 40.7128, -74.0060
#         else:
#             address = st.text_input("Enter your address:")
#             if address:
#                 geolocator = Nominatim(user_agent="pediatric-symptom-checker")
#                 try:
#                     location = geolocator.geocode(address)
#                     lat, lon = location.latitude, location.longitude
#                 except Exception as e:
#                     st.error(f"Geocoding error: {e}")
#                     lat, lon = 40.7128, -74.0060
#             else:
#                 lat, lon = 40.7128, -74.0060
#         search_radius = st.slider("Search radius (meters)", 500, 10000, 2000)
#         if st.button("Find Nearby Doctors", key="find_doctors"):
#             with st.spinner("Searching for nearby doctors..."):
#                 doctors_df = find_nearby_doctors(lat, lon, search_radius)
#                 if not doctors_df.empty:
#                     st.success(f"Found {len(doctors_df)} doctors/clinics nearby")
#                     m = folium.Map(location=[lat, lon], zoom_start=13)
#                     folium.Marker([lat, lon], popup="Your Location", icon=folium.Icon(color="blue", icon="user")).add_to(m)
#                     for idx, row in doctors_df.iterrows():
#                         popup_text = f"<b>{row['name']}</b><br><i>{row['specialty']}</i><br>{row['address']}"
#                         icon_color = "green" if "pediatric" in row['specialty'].lower() else "red"
#                         folium.Marker([row['latitude'], row['longitude']], popup=popup_text, icon=folium.Icon(color=icon_color, icon="medkit")).add_to(m)
#                     folium_static(m)
#                     st.subheader("Nearby Healthcare Providers")
#                     st.dataframe(doctors_df[['name', 'specialty', 'address']])
#                 else:
#                     st.warning("No doctors found in the specified area. Try increasing the search radius.")

# # Train the model
# @st.cache_resource
# def train_model(df):
#     # Add AGE_FEATURE and IMMUNOCOMPROMISED_FEATURE columns (default to 0 for training)
#     df["AGE_FEATURE"] = 0
#     df["IMMUNOCOMPROMISED_FEATURE"] = 0

#     # Encode target variable
#     label_encoder = LabelEncoder()
#     df["CONDITION"] = label_encoder.fit_transform(df["CONDITION"])

#     # Separate features and target
#     X = df.drop(columns=["CONDITION"])
#     y = df["CONDITION"]

#     # Split data
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

#     # Create pipeline with scaling and classifier
#     pipeline = Pipeline([
#         ("scaler", StandardScaler()),
#         ("classifier", RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))
#     ])

#     # Train model
#     pipeline.fit(X_train, y_train)

#     # Evaluate model
#     y_pred = pipeline.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     st.success(f"Model trained with accuracy: {accuracy:.2%}")

#     return pipeline, label_encoder


# # Main application
# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
#     st.title("👶 Pediatric Symptom Checker")

#     # Load data
#     file_path = "pages/pediatric_dataset_30k.csv"  # Replace with your actual file path
#     df = load_data(file_path)

#     # Train model
#     model, label_encoder = train_model(df)

#     # Get all available symptoms from dataset
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]

#     # Age input
#     with st.expander("Patient Information", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Age (months)", min_value=0, max_value=216, value=24, step=1)
#         with col2:
#             medical_history = st.multiselect("Medical History (select all that apply)",
#                                              options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                                              default=[])

#     # Step 1: Primary symptom selection
#     with st.expander("Step 1: Select main symptoms", expanded=True):
#         primary_symptoms = st.multiselect("What symptoms is your child experiencing?",
#                                           options=all_symptoms,
#                                           placeholder="Select symptoms...")

#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("Step 2: Provide symptom details", expanded=True):
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS:
#                     st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
#                     symptom_score = 0  # Base score
#                     for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                         response = None
#                         if question["type"] == "radio":
#                             response = st.radio(question["question"],
#                                                 options=question["options"],
#                                                 key=f"{symptom}_{question['question']}")
#                         elif question["type"] == "selectbox":
#                             response = st.selectbox(question["question"],
#                                                     options=question["options"],
#                                                     key=f"{symptom}_{question['question']}")
#                         elif question["type"] == "checkbox":
#                             response = st.multiselect(question["question"],
#                                                       options=question["options"],
#                                                       key=f"{symptom}_{question['question']}")
#                         if response:
#                             if isinstance(response, list):  # For checkbox questions
#                                 for item in response:
#                                     symptom_score += question["weights"][item]
#                             else:  # For radio/selectbox
#                                 symptom_score += question["weights"][response]
#                     symptom_details[symptom] = symptom_score
#                 else:
#                     # For symptoms without follow-up questions
#                     severity = st.slider(f"Severity of {symptom.lower().replace('_', ' ')}",
#                                          min_value=0.1, max_value=3.0, value=1.0, step=0.1, key=symptom)
#                     symptom_details[symptom] = severity

#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return

#         # Prepare input features
#         input_features = {col: 0.0 for col in all_symptoms}
#         input_features["AGE_FEATURE"] = 0
#         input_features["IMMUNOCOMPROMISED_FEATURE"] = 0

#         # Apply symptom scores
#         for symptom, score in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = score

#         # Add age as a feature
#         def calculate_age_feature(age):
#             if age < 3:
#                 return 3  # Higher risk for infants
#             elif age < 12:
#                 return 2  # Moderate risk for young children
#             else:
#                 return 1  # Lower risk for older children

#         input_features["AGE_FEATURE"] = calculate_age_feature(age)

#         # Add medical history as a feature
#         if "Immunocompromised" in medical_history:
#             input_features["IMMUNOCOMPROMISED_FEATURE"] = 1
#         else:
#             input_features["IMMUNOCOMPROMISED_FEATURE"] = 0

#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])

#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]

#         # Decode prediction back to disease name
#         prediction = label_encoder.inverse_transform([prediction])[0]

#         # Red flags
#         red_flags = []
#         for symptom in primary_symptoms:
#             if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                 red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])

#         # Recommendations
#         #jee
#         recommendations = []
#         if "Meningitis" in prediction:
#             recommendations.append("EMERGENCY: Seek immediate medical attention - This is a medical emergency requiring IV antibiotics.")
#         if "Immunocompromised" in medical_history:
#             recommendations.append("Children with compromised immune systems should be evaluated earlier for infections.")

#         # Display results
#         st.success(f"### Most likely condition: **{prediction}**")
#         st.subheader("Top Possible Conditions")
#         prob_df = pd.DataFrame({"Condition": label_encoder.classes_,
#                                 "Probability": probabilities}).sort_values("Probability", ascending=False)
#         st.dataframe(prob_df.style.format({"Probability": "{:.2%}"}), hide_index=True)

#         # Show red flags
#         if red_flags:
#             st.subheader("⚠️ Red Flags to Watch For")
#             for flag in red_flags:
#                 st.error(f"• {flag}")
#         else:
#             st.subheader("ℹ️ No Urgent Red Flags")
#             st.info("No urgent red flags identified based on current symptoms")

#         # Show recommendations
#         st.subheader("ℹ️ Recommended Actions")
#         for rec in recommendations:
#             st.warning(rec)

#     # Generate PDF report
#         pdf = generate_pdf_report(
#             patient_info={
#                 "age": age,
#                 "medical_history": medical_history
#             },
#             symptoms=symptom_details,
#             prediction=prediction,
#             probabilities_df=prob_df,
#             red_flags=red_flags,
#             recommendations=recommendations
#         )
        
#         # Create download link
#         pdf_output = pdf.output(dest='S').encode('latin-1')
#         b64 = base64.b64encode(pdf_output).decode()
#         href = f'<a href="data:application/octet-stream;base64,{b64}" download="pediatric_health_report.pdf">Download Full Medical Report as PDF</a>'
#         st.markdown(href, unsafe_allow_html=True)

#     # Show nearby doctors feature (always visible)
#     show_nearby_doctors()

# if __name__ == "__main__":
#     main()



#correct colors

# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.pipeline import Pipeline
# import requests
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# from fpdf import FPDF
# import base64
# from datetime import datetime
# import time

# # Custom CSS for modern UI
# def local_css():
#     st.markdown("""
#     <style>
#         :root {
#             --primary: #4a6fa5;
#             --secondary: #166088;
#             --accent: #4fc1e9;
#             --background: #f8f9fa;
#             --card: #ffffff;
#             --text: #2c3e50;
#             --warning: #ff6b6b;
#             --success: #48dbb4;
#         }
        
#         .main {
#             background-color: var(--background);
#         }
        
#         /* Header styling */
#         .header-container {
#             background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
#             padding: 2rem;
#             border-radius: 12px;
#             margin-bottom: 2rem;
#             box-shadow: 0 4px 20px rgba(0,0,0,0.1);
#             color: white;
#             text-align: center;
#         }
        
#         /* Button styling */
#         .stButton>button {
#             background-color: var(--primary);
#             color: white;
#             border-radius: 8px;
#             padding: 0.75rem 1.5rem;
#             font-weight: 600;
#             border: none;
#             transition: all 0.3s ease;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#         }
        
#         .stButton>button:hover {
#             background-color: var(--secondary);
#             transform: translateY(-2px);
#             box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#         }
        
#         .stButton>button:active {
#             transform: translateY(0);
#         }
        
#         /* Progress bar */
#         .stProgress > div > div > div > div {
#             background-color: var(--accent);
#         }
        
#         /* Cards */
#         .card {
#             background-color: var(--card);
#             border-radius: 12px;
#             padding: 1.5rem;
#             margin-bottom: 1rem;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#             border: 1px solid rgba(0,0,0,0.05);
#         }
        
#         /* Expander styling */
#         .streamlit-expanderHeader {
#             font-weight: 600;
#             color: var(--primary);
#         }
        
#         /* Alert boxes */
#         .stAlert {
#             border-radius: 12px;
#         }
        
#         /* Custom components */
#         .symptom-card {
#             background-color: var(--card);
#             border-radius: 12px;
#             padding: 1.25rem;
#             margin-bottom: 1rem;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.05);
#             transition: all 0.3s ease;
#         }
        
#         .symptom-card:hover {
#             box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#             transform: translateY(-2px);
#         }
        
#         .red-flag {
#             background-color: rgba(255,107,107,0.1);
#             border-left: 4px solid var(--warning);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#             animation: pulse 2s infinite;
#         }
        
#         .recommendation {
#             background-color: rgba(72,219,180,0.1);
#             border-left: 4px solid var(--success);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#         }
        
#         .diagnosis-highlight {
#             background: linear-gradient(135deg, rgba(74,111,165,0.1) 0%, rgba(22,96,136,0.1) 100%);
#             padding: 1.5rem;
#             border-radius: 12px;
#             margin-bottom: 1.5rem;
#             border: 1px solid rgba(74,111,165,0.2);
#         }
        
#         @keyframes pulse {
#             0% { box-shadow: 0 0 0 0 rgba(255,107,107,0.4); }
#             70% { box-shadow: 0 0 0 10px rgba(255,107,107,0); }
#             100% { box-shadow: 0 0 0 0 rgba(255,107,107,0); }
#         }
        
#         /* Tabs */
#         .stTabs [data-baseweb="tab-list"] {
#             gap: 10px;
#         }
        
#         .stTabs [data-baseweb="tab"] {
#             height: 50px;
#             padding: 0 20px;
#             background-color: #f0f4f8;
#             border-radius: 8px 8px 0 0 !important;
#             font-weight: 500;
#             transition: all 0.2s ease;
#         }
        
#         .stTabs [data-baseweb="tab"]:hover {
#             background-color: #e1e8f0;
#         }
        
#         .stTabs [aria-selected="true"] {
#             background-color: var(--primary) !important;
#             color: white !important;
#         }
        
#         /* Input fields */
#         .stTextInput input, .stNumberInput input, .stSelectbox select {
#             border-radius: 8px !important;
#             padding: 10px 12px !important;
#         }
        
#         /* Radio buttons */
#         .stRadio [role="radiogroup"] {
#             gap: 15px;
#         }
        
#         .stRadio [role="radio"] {
#             padding: 8px 16px;
#             border-radius: 8px;
#             border: 1px solid #dfe3e8;
#         }
        
#         .stRadio [role="radio"][aria-checked="true"] {
#             background-color: var(--primary);
#             color: white;
#             border-color: var(--primary);
#         }
        
#         /* Sliders */
#         .stSlider [role="slider"] {
#             background-color: var(--primary) !important;
#         }
        
#         /* Footer */
#         .footer {
#             text-align: center;
#             padding: 1.5rem;
#             color: #666;
#             font-size: 0.9em;
#             margin-top: 2rem;
#             border-top: 1px solid #eee;
#         }
        
#         /* Responsive adjustments */
#         @media (max-width: 768px) {
#             .header-container {
#                 padding: 1.5rem 1rem;
#             }
            
#             .stButton>button {
#                 padding: 0.5rem 1rem;
#             }
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # PDF Report Generator
# def generate_pdf_report(patient_info, symptoms, prediction, probabilities_df, red_flags, recommendations):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 16)
    
#     # Header with color
#     pdf.set_fill_color(74, 111, 165)
#     pdf.set_text_color(255, 255, 255)
#     pdf.cell(0, 10, "Pediatric Health Report", 0, 1, 'C', 1)
#     pdf.set_font("Arial", '', 10)
#     pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C', 1)
#     pdf.ln(10)
    
#     # Reset colors
#     pdf.set_fill_color(255, 255, 255)
#     pdf.set_text_color(0, 0, 0)
    
#     # Patient Information
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Patient Information", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     pdf.cell(0, 8, f"Age: {patient_info['age']} months", 0, 1)
#     pdf.cell(0, 8, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", 0, 1)
#     pdf.ln(5)
    
#     # Symptoms
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Reported Symptoms", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     for symptom, details in symptoms.items():
#         pdf.cell(0, 8, f"- {symptom.replace('_', ' ').title()}: Severity score {details}", 0, 1)
#     pdf.ln(5)
    
#     # Diagnosis
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Diagnostic Assessment", 0, 1)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.set_text_color(74, 111, 165)  # Primary color
#     pdf.cell(0, 8, f"Most Likely Condition: {prediction}", 0, 1)
#     pdf.set_text_color(0, 0, 0)
#     pdf.set_font("Arial", '', 12)
    
#     # Probability table
#     pdf.cell(0, 8, "Condition Probabilities:", 0, 1)
#     col_width = pdf.w / 3
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(col_width, 8, "Condition", 1)
#     pdf.cell(col_width, 8, "Probability", 1, 1)
#     pdf.set_font("Arial", '', 12)
    
#     for _, row in probabilities_df.iterrows():
#         pdf.cell(col_width, 8, row['Condition'], 1)
#         pdf.cell(col_width, 8, f"{row['Probability']:.2%}", 1, 1)
#     pdf.ln(5)
    
#     # Red Flags
#     if red_flags:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.set_text_color(255, 107, 107)  # Warning color
#         pdf.cell(0, 10, "Red Flags", 0, 1)
#         pdf.set_text_color(0, 0, 0)
#         pdf.set_font("Arial", '', 12)
#         for flag in red_flags:
#             pdf.cell(0, 8, f"- {flag}", 0, 1)
#         pdf.ln(5)
    
#     # Recommendations
#     if recommendations:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.set_text_color(72, 219, 180)  # Success color
#         pdf.cell(0, 10, "Recommendations", 0, 1)
#         pdf.set_text_color(0, 0, 0)
#         pdf.set_font("Arial", '', 12)
#         for rec in recommendations:
#             pdf.cell(0, 8, f"- {rec}", 0, 1)
#         pdf.ln(5)
    
#     # Disclaimer
#     pdf.set_font("Arial", 'I', 10)
#     pdf.multi_cell(0, 8, "Disclaimer: This report is generated by an AI system and should not replace professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
    
#     return pdf

# # Load and preprocess the dataset
# @st.cache_data
# def load_data(file_path):
#     df = pd.read_csv(file_path)
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# # Enhanced medical knowledge base
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio",
#              "options": ["<100.4°F", "100.4-102.2°F", "102.2-104°F", ">104°F"],
#              "weights": {"<100.4°F": 1, "100.4-102.2°F": 2, "102.2-104°F": 3, ">104°F": 4}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 1, "1-3 days": 2, "3-7 days": 3, ">7 days": 4}}
#         ],
#         "red_flags": ["Fever >100.4°F in infants <3 months", "Fever >104°F"]
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping"],
#              "weights": {"Dry": 1, "Productive": 2, "Barking": 3, "Whooping": 4}},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1, "Nighttime": 2, "With feeding": 2, "After exercise": 2, "All day": 3}}
#         ],
#         "red_flags": ["Whooping sound on inspiration", "Cough causing vomiting"]
#     },
#     "RUNNY_NOSE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Nasal discharge with foul odor"]
#     },
#     "SNEEZING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["Occasional", "Frequent", "Constant"],
#              "weights": {"Occasional": 1, "Frequent": 2, "Constant": 3}}
#         ]
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1, "5-8 loose stools/day": 2, ">8 loose stools/day": 3, "Watery": 3}},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1, "Mucoid": 2, "Bloody": 3, "Rice-water": 3}}
#         ]
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1, "No tears": 2, "Sunken eyes": 3, "Decreased urine output": 3, "Lethargy": 4}}
#         ],
#         "red_flags": ["Severe dehydration signs"]
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3, "Doubled over": 4}}
#         ]
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Macular", "Papular", "Vesicular", "Petechial/Purpuric"],
#              "weights": {"Macular": 1, "Papular": 2, "Vesicular": 3, "Petechial/Purpuric": 4}}
#         ]
#     },
#     "HEADACHE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Severe headache with fever", "Headache with neck stiffness"]
#     }
# }

# # Find nearby doctors using Overpass API
# def find_nearby_doctors(lat, lon, radius=5000):
#     overpass_url = "https://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json];
#     (
#         node["amenity"="doctors"](around:{radius},{lat},{lon});
#         node["amenity"="clinic"](around:{radius},{lat},{lon});
#         node["healthcare"="doctor"](around:{radius},{lat},{lon});
#         node["healthcare"="pediatrician"](around:{radius},{lat},{lon});
#     );
#     out center;
#     """
#     try:
#         response = requests.get(overpass_url, params={'data': query})
#         response.raise_for_status()
#         data = response.json()
#         doctors = []
#         for element in data['elements']:
#             name = element.get('tags', {}).get('name', 'Unknown')
#             address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Address not available'))
#             specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
#             lat = element.get('lat', element.get('center', {}).get('lat'))
#             lon = element.get('lon', element.get('center', {}).get('lon'))
#             if lat and lon:
#                 doctors.append({'name': name, 'address': address, 'specialty': specialty, 'latitude': lat, 'longitude': lon})
#         return pd.DataFrame(doctors)
#     except Exception as e:
#         st.error(f"Error fetching nearby doctors: {e}")
#         return pd.DataFrame()

# # Show nearby doctors interface
# def show_nearby_doctors():
#     with st.expander("🚑 Find Nearby Pediatricians & Clinics", expanded=False):
#         st.markdown("### 🔍 Locate healthcare providers near you")
        
#         tab1, tab2 = st.tabs(["📍 Use Current Location", "🏠 Enter Address"])
        
#         with tab1:
#             st.info("We'll use your approximate location (no precise data is stored)")
#             if st.button("Detect My Location", key="detect_loc"):
#                 try:
#                     loc = st.experimental_get_query_params().get("location", None)
#                     if loc:
#                         lat, lon = map(float, loc[0].split(","))
#                         st.success(f"Location detected: {lat:.4f}, {lon:.4f}")
#                     else:
#                         st.warning("Couldn't detect location. Using default.")
#                         lat, lon = 40.7128, -74.0060
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     lat, lon = 40.7128, -74.0060
        
#         with tab2:
#             address = st.text_input("Enter your full address:", placeholder="e.g., 123 Main St, City, Country")
#             if address:
#                 geolocator = Nominatim(user_agent="pediatric-symptom-checker")
#                 try:
#                     location = geolocator.geocode(address)
#                     if location:
#                         lat, lon = location.latitude, location.longitude
#                         st.success(f"Found location: {lat:.4f}, {lon:.4f}")
#                     else:
#                         st.warning("Address not found. Using default.")
#                         lat, lon = 40.7128, -74.0060
#                 except Exception as e:
#                     st.error(f"Geocoding error: {e}")
#                     lat, lon = 40.7128, -74.0060
#             else:
#                 lat, lon = 40.7128, -74.0060
        
#         search_radius = st.slider("Search radius (meters)", 500, 10000, 2000, help="Wider radius may show more options")
        
#         if st.button("🔍 Search for Doctors", type="primary", use_container_width=True):
#             with st.spinner("Searching nearby..."):
#                 doctors_df = find_nearby_doctors(lat, lon, search_radius)
#                 if not doctors_df.empty:
#                     st.success(f"✅ Found {len(doctors_df)} healthcare providers nearby")
                    
#                     # Create map
#                     m = folium.Map(location=[lat, lon], zoom_start=13, tiles="cartodbpositron")
#                     folium.Marker(
#                         [lat, lon], 
#                         popup="Your Location", 
#                         icon=folium.Icon(color="blue", icon="user", prefix="fa")
#                     ).add_to(m)
                    
#                     # Add doctors
#                     for idx, row in doctors_df.iterrows():
#                         is_pediatric = "pediatric" in str(row['specialty']).lower()
#                         icon_color = "green" if is_pediatric else "red"
#                         icon_type = "child" if is_pediatric else "user-md"
                        
#                         folium.Marker(
#                             [row['latitude'], row['longitude']],
#                             popup=f"<b>{row['name']}</b><br><i>{row['specialty']}</i><br>{row['address']}",
#                             icon=folium.Icon(color=icon_color, icon=icon_type, prefix="fa")
#                         ).add_to(m)
                    
#                     # Display
#                     folium_static(m, width=700, height=500)
                    
#                     # Show table
#                     st.markdown("### 🏥 Nearby Healthcare Providers")
#                     st.dataframe(
#                         doctors_df[['name', 'specialty', 'address']].rename(columns={
#                             'name': 'Name',
#                             'specialty': 'Specialty',
#                             'address': 'Address'
#                         }),
#                         hide_index=True,
#                         use_container_width=True
#                     )
#                 else:
#                     st.warning("No doctors found in this area. Try increasing the search radius.")

# # Train the model
# @st.cache_resource
# def train_model(df):
#     df["AGE_FEATURE"] = 0
#     df["IMMUNOCOMPROMISED_FEATURE"] = 0
#     label_encoder = LabelEncoder()
#     df["CONDITION"] = label_encoder.fit_transform(df["CONDITION"])
#     X = df.drop(columns=["CONDITION"])
#     y = df["CONDITION"]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
#     pipeline = Pipeline([
#         ("scaler", StandardScaler()),
#         ("classifier", RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))
#     ])
#     pipeline.fit(X_train, y_train)
#     y_pred = pipeline.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     return pipeline, label_encoder

# # Main application
# def main():
#     st.set_page_config(
#         page_title="Pediatric Symptom Checker", 
#         page_icon="👶", 
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )
#     local_css()
    
#     # Header with gradient
#     st.markdown("""
#     <div class="header-container">
#         <h1 style="margin:0;padding:0;">👶 Pediatric Symptom Checker</h1>
#         <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">A smart tool to help parents assess their child's symptoms and get guidance</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Introduction
#     st.markdown("""
#     <div class="card">
#         <p>Welcome to the Pediatric Symptom Checker. This tool helps you evaluate your child's symptoms and provides 
#         guidance on possible conditions. Please follow these steps:</p>
#         <ol>
#             <li>Provide basic information about your child</li>
#             <li>Select all symptoms your child is experiencing</li>
#             <li>Provide details about each symptom</li>
#             <li>Get an assessment with recommendations</li>
#         </ol>
#         <p><strong>Remember:</strong> This tool doesn't replace professional medical advice.</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Load data and model
#     file_path = "pages/pediatric_dataset_30k.csv"
#     df = load_data(file_path)
#     model, label_encoder = train_model(df)
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
#     # Step 1: Patient Information
#     with st.expander("👤 Step 1: Patient Information", expanded=True):
#         st.markdown("### Tell us about your child")
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input(
#                 "Age (months)", 
#                 min_value=0, 
#                 max_value=216, 
#                 value=24, 
#                 step=1,
#                 help="Child's age in months (0-18 years)"
#             )
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                 default=[],
#                 help="Any pre-existing conditions"
#             )
    
#     # Step 2: Symptom Selection
#     with st.expander("🤒 Step 2: Select Symptoms", expanded=False):
#         st.markdown("### What symptoms is your child experiencing?")
#         primary_symptoms = st.multiselect(
#             "Select all that apply:",
#             options=all_symptoms,
#             placeholder="Choose symptoms...",
#             help="Start typing to search symptoms"
#         )
    
#     # Step 3: Symptom Details
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("📝 Step 3: Symptom Details", expanded=False):
#             st.markdown("### Provide more details about each symptom")
#             progress_bar = st.progress(0)
#             total_symptoms = len(primary_symptoms)
            
#             for i, symptom in enumerate(primary_symptoms):
#                 with st.container():
#                     st.markdown(f"<div class='symptom-card'><h4>{symptom.replace('_', ' ').title()}</h4></div>", unsafe_allow_html=True)
                    
#                     if symptom in SYMPTOM_DEFINITIONS:
#                         symptom_score = 0
#                         for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                             if question["type"] == "radio":
#                                 response = st.radio(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}",
#                                     horizontal=True
#                                 )
#                                 symptom_score += question["weights"][response]
#                             elif question["type"] == "selectbox":
#                                 response = st.selectbox(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}"
#                                 )
#                                 symptom_score += question["weights"][response]
#                             elif question["type"] == "checkbox":
#                                 response = st.multiselect(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}"
#                                 )
#                                 for item in response:
#                                     symptom_score += question["weights"][item]
#                         symptom_details[symptom] = symptom_score
#                     else:
#                         severity = st.slider(
#                             f"Severity of {symptom.replace('_', ' ')}",
#                             min_value=0.1, 
#                             max_value=3.0, 
#                             value=1.0, 
#                             step=0.1, 
#                             key=symptom,
#                             help="1 = Mild, 3 = Severe"
#                         )
#                         symptom_details[symptom] = severity
                    
#                     progress_bar.progress((i + 1) / total_symptoms)
#                     if i < total_symptoms - 1:
#                         st.divider()
    
#     # Step 4: Analysis
#     if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             st.stop()
        
#         with st.spinner("Analyzing symptoms..."):
#             # Add a slight delay for better UX
#             time.sleep(1)
            
#             # Prepare input features
#             input_features = {col: 0.0 for col in all_symptoms}
#             input_features["AGE_FEATURE"] = 3 if age < 3 else (2 if age < 12 else 1)
#             input_features["IMMUNOCOMPROMISED_FEATURE"] = 1 if "Immunocompromised" in medical_history else 0
            
#             for symptom, score in symptom_details.items():
#                 if symptom in input_features:
#                     input_features[symptom] = score
            
#             # Make prediction
#             input_df = pd.DataFrame([input_features])
#             prediction = model.predict(input_df)[0]
#             probabilities = model.predict_proba(input_df)[0]
#             prediction = label_encoder.inverse_transform([prediction])[0]
            
#             # Get red flags
#             red_flags = []
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])
            
#             # Generate recommendations
#             recommendations = []
#             if "Meningitis" in prediction:
#                 recommendations.append("EMERGENCY: Seek immediate medical attention - This is a medical emergency requiring IV antibiotics.")
#             if "Immunocompromised" in medical_history:
#                 recommendations.append("Children with compromised immune systems should be evaluated earlier for infections.")
            
#             # Display results
#             st.markdown("---")
#             st.markdown(f"""
#             <div class='diagnosis-highlight'>
#                 <h2 style='text-align:center;margin-bottom:0.5rem;'>Diagnostic Results</h2>
#                 <h3 style='text-align:center;color:#4a6fa5;margin-top:0;'>Most likely condition: {prediction}</h3>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Condition probabilities
#             st.markdown("### Condition Probabilities")
#             prob_df = pd.DataFrame({
#                 "Condition": label_encoder.classes_,
#                 "Probability": probabilities
#             }).sort_values("Probability", ascending=False)
            
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"}),
#                 column_config={
#                     "Condition": "Possible Condition",
#                     "Probability": st.column_config.ProgressColumn(
#                         "Probability",
#                         help="How likely this condition is",
#                         format="%.2f%%",
#                         min_value=0,
#                         max_value=1,
#                     )
#                 },
#                 hide_index=True,
#                 use_container_width=True
#             )
            
#             # Red flags
#             if red_flags:
#                 st.markdown("### ⚠️ Red Flags")
#                 for flag in red_flags:
#                     st.markdown(f"""
#                     <div class='red-flag'>
#                         <p style='margin:0;'><strong>{flag}</strong></p>
#                     </div>
#                     """, unsafe_allow_html=True)
#             else:
#                 st.markdown("""
#                 <div class='card' style='background-color:#e8f5e9;'>
#                     <h4 style='color:#2e7d32;margin:0;'>No urgent red flags identified</h4>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # Recommendations
#             if recommendations:
#                 st.markdown("### Recommended Actions")
#                 for rec in recommendations:
#                     st.markdown(f"""
#                     <div class='recommendation'>
#                         <p style='margin:0;'>{rec}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
            
#             # PDF Report
#             st.markdown("---")
#             st.markdown("### 📄 Download Report")
#             pdf = generate_pdf_report(
#                 patient_info={"age": age, "medical_history": medical_history},
#                 symptoms=symptom_details,
#                 prediction=prediction,
#                 probabilities_df=prob_df,
#                 red_flags=red_flags,
#                 recommendations=recommendations
#             )
            
#             pdf_output = pdf.output(dest='S').encode('latin-1')
#             b64 = base64.b64encode(pdf_output).decode()
#             href = f"""
#             <a href="data:application/octet-stream;base64,{b64}" download="pediatric_health_report.pdf" style='
#                 display: inline-block;
#                 background-color: #4a6fa5;
#                 color: white;
#                 padding: 12px 24px;
#                 text-align: center;
#                 text-decoration: none;
#                 font-size: 16px;
#                 margin: 4px 2px;
#                 cursor: pointer;
#                 border-radius: 8px;
#                 border: none;
#                 transition: all 0.3s ease;
#             ' onmouseover="this.style.backgroundColor='#166088'" onmouseout="this.style.backgroundColor='#4a6fa5'">📥 Download Full Medical Report</a>
#             """
#             st.markdown(href, unsafe_allow_html=True)
    
#     # Nearby doctors section
#     st.markdown("---")
#     show_nearby_doctors()
    
#     # Footer
#     st.markdown("""
#     <div class="footer">
#         <p>This tool is for informational purposes only and does not provide medical advice.</p>
#         <p>Always consult a qualified healthcare provider for diagnosis and treatment.</p>
#     </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

#ui


# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.pipeline import Pipeline
# import requests
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# from fpdf import FPDF
# import base64
# from datetime import datetime
# import time
# import random

# # Custom CSS for modern UI
# def local_css():
#     st.markdown("""
#     <style>
#         :root {
#             --primary: #4a6fa5;
#             --secondary: #166088;
#             --accent: #4fc1e9;
#             --background: #f8f9fa;
#             --card: #ffffff;
#             --text: #2c3e50;
#             --warning: #ff6b6b;
#             --success: #48dbb4;
#             --info: #5bc0de;
#         }
        
#         .main {
#             background-color: var(--background);
#         }
        
#         /* Header styling */
#         .header-container {
#             background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
#             padding: 2rem;
#             border-radius: 12px;
#             margin-bottom: 2rem;
#             box-shadow: 0 4px 20px rgba(0,0,0,0.1);
#             color: white;
#             text-align: center;
#         }
        
#         /* Button styling */
#         .stButton>button {
#             background-color: var(--primary);
#             color: white;
#             border-radius: 8px;
#             padding: 0.75rem 1.5rem;
#             font-weight: 600;
#             border: none;
#             transition: all 0.3s ease;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#         }
        
#         .stButton>button:hover {
#             background-color: var(--secondary);
#             transform: translateY(-2px);
#             box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#         }
        
#         .stButton>button:active {
#             transform: translateY(0);
#         }
        
#         /* Primary button */
#         .primary-button {
#             background-color: var(--primary) !important;
#             color: white !important;
#         }
        
#         /* Secondary button */
#         .secondary-button {
#             background-color: var(--secondary) !important;
#             color: white !important;
#         }
        
#         /* Progress bar */
#         .stProgress > div > div > div > div {
#             background-color: var(--accent);
#         }
        
#         /* Cards */
#         .card {
#             background-color: var(--card);
#             border-radius: 12px;
#             padding: 1.5rem;
#             margin-bottom: 1rem;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#             border: 1px solid rgba(0,0,0,0.05);
#         }
        
#         /* Expander styling */
#         .streamlit-expanderHeader {
#             font-weight: 600;
#             color: var(--primary);
#             font-size: 1.1rem;
#         }
        
#         .streamlit-expanderContent {
#             padding: 1rem 1.5rem;
#         }
        
#         /* Alert boxes */
#         .stAlert {
#             border-radius: 12px;
#         }
        
#         /* Custom components */
#         .symptom-card {
#             background-color: var(--card);
#             border-radius: 12px;
#             padding: 1.25rem;
#             margin-bottom: 1rem;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.05);
#             transition: all 0.3s ease;
#             border-left: 4px solid var(--accent);
#         }
        
#         .symptom-card:hover {
#             box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#             transform: translateY(-2px);
#         }
        
#         .red-flag {
#             background-color: rgba(255,107,107,0.1);
#             border-left: 4px solid var(--warning);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#             animation: pulse 2s infinite;
#         }
        
#         .recommendation {
#             background-color: rgba(72,219,180,0.1);
#             border-left: 4px solid var(--success);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#         }
        
#         .info-card {
#             background-color: rgba(91,192,222,0.1);
#             border-left: 4px solid var(--info);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#         }
        
#         .diagnosis-highlight {
#             background: linear-gradient(135deg, rgba(74,111,165,0.1) 0%, rgba(22,96,136,0.1) 100%);
#             padding: 1.5rem;
#             border-radius: 12px;
#             margin-bottom: 1.5rem;
#             border: 1px solid rgba(74,111,165,0.2);
#         }
        
#         @keyframes pulse {
#             0% { box-shadow: 0 0 0 0 rgba(255,107,107,0.4); }
#             70% { box-shadow: 0 0 0 10px rgba(255,107,107,0); }
#             100% { box-shadow: 0 0 0 0 rgba(255,107,107,0); }
#         }
        
#         /* Tabs */
#         .stTabs [data-baseweb="tab-list"] {
#             gap: 10px;
#         }
        
#         .stTabs [data-baseweb="tab"] {
#             height: 50px;
#             padding: 0 20px;
#             background-color: #f0f4f8;
#             border-radius: 8px 8px 0 0 !important;
#             font-weight: 500;
#             transition: all 0.2s ease;
#         }
        
#         .stTabs [data-baseweb="tab"]:hover {
#             background-color: #e1e8f0;
#         }
        
#         .stTabs [aria-selected="true"] {
#             background-color: var(--primary) !important;
#             color: white !important;
#         }
        
#         /* Input fields */
#         .stTextInput input, .stNumberInput input, .stSelectbox select {
#             border-radius: 8px !important;
#             padding: 10px 12px !important;
#         }
        
#         /* Radio buttons */
#         .stRadio [role="radiogroup"] {
#             gap: 15px;
#         }
        
#         .stRadio [role="radio"] {
#             padding: 8px 16px;
#             border-radius: 8px;
#             border: 1px solid #dfe3e8;
#         }
        
#         .stRadio [role="radio"][aria-checked="true"] {
#             background-color: var(--primary);
#             color: white;
#             border-color: var(--primary);
#         }
        
#         /* Sliders */
#         .stSlider [role="slider"] {
#             background-color: var(--primary) !important;
#         }
        
#         /* Footer */
#         .footer {
#             text-align: center;
#             padding: 1.5rem;
#             color: #666;
#             font-size: 0.9em;
#             margin-top: 2rem;
#             border-top: 1px solid #eee;
#         }
        
#         /* Tooltips */
#         .stTooltip {
#             border-radius: 8px !important;
#             padding: 8px 12px !important;
#         }
        
#         /* Responsive adjustments */
#         @media (max-width: 768px) {
#             .header-container {
#                 padding: 1.5rem 1rem;
#             }
            
#             .stButton>button {
#                 padding: 0.5rem 1rem;
#             }
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # PDF Report Generator
# def generate_pdf_report(patient_info, symptoms, prediction, probabilities_df, red_flags, recommendations):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 16)
    
#     # Header with color
#     pdf.set_fill_color(74, 111, 165)
#     pdf.set_text_color(255, 255, 255)
#     pdf.cell(0, 10, "Pediatric Health Report", 0, 1, 'C', 1)
#     pdf.set_font("Arial", '', 10)
#     pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C', 1)
#     pdf.ln(10)
    
#     # Reset colors
#     pdf.set_fill_color(255, 255, 255)
#     pdf.set_text_color(0, 0, 0)
    
#     # Patient Information
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Patient Information", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     pdf.cell(0, 8, f"Age: {patient_info['age']} months", 0, 1)
#     pdf.cell(0, 8, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", 0, 1)
#     pdf.ln(5)
    
#     # Symptoms
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Reported Symptoms", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     for symptom, details in symptoms.items():
#         pdf.cell(0, 8, f"- {symptom.replace('_', ' ').title()}: Severity score {details}", 0, 1)
#     pdf.ln(5)
    
#     # Diagnosis
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Diagnostic Assessment", 0, 1)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.set_text_color(74, 111, 165)  # Primary color
#     pdf.cell(0, 8, f"Most Likely Condition: {prediction}", 0, 1)
#     pdf.set_text_color(0, 0, 0)
#     pdf.set_font("Arial", '', 12)
    
#     # Probability table
#     pdf.cell(0, 8, "Condition Probabilities:", 0, 1)
#     col_width = pdf.w / 3
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(col_width, 8, "Condition", 1)
#     pdf.cell(col_width, 8, "Probability", 1, 1)
#     pdf.set_font("Arial", '', 12)
    
#     for _, row in probabilities_df.iterrows():
#         pdf.cell(col_width, 8, row['Condition'], 1)
#         pdf.cell(col_width, 8, f"{row['Probability']:.2%}", 1, 1)
#     pdf.ln(5)
    
#     # Red Flags
#     if red_flags:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.set_text_color(255, 107, 107)  # Warning color
#         pdf.cell(0, 10, "Red Flags", 0, 1)
#         pdf.set_text_color(0, 0, 0)
#         pdf.set_font("Arial", '', 12)
#         for flag in red_flags:
#             pdf.cell(0, 8, f"- {flag}", 0, 1)
#         pdf.ln(5)
    
#     # Recommendations
#     if recommendations:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.set_text_color(72, 219, 180)  # Success color
#         pdf.cell(0, 10, "Recommendations", 0, 1)
#         pdf.set_text_color(0, 0, 0)
#         pdf.set_font("Arial", '', 12)
#         for rec in recommendations:
#             pdf.cell(0, 8, f"- {rec}", 0, 1)
#         pdf.ln(5)
    
#     # Disclaimer
#     pdf.set_font("Arial", 'I', 10)
#     pdf.multi_cell(0, 8, "Disclaimer: This report is generated by an AI system and should not replace professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
    
#     return pdf

# # Load and preprocess the dataset
# @st.cache_data
# def load_data(file_path):
#     df = pd.read_csv(file_path)
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# # Enhanced medical knowledge base
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio",
#              "options": ["<100.4°F", "100.4-102.2°F", "102.2-104°F", ">104°F"],
#              "weights": {"<100.4°F": 1, "100.4-102.2°F": 2, "102.2-104°F": 3, ">104°F": 4}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 1, "1-3 days": 2, "3-7 days": 3, ">7 days": 4}}
#         ],
#         "red_flags": ["Fever >100.4°F in infants <3 months", "Fever >104°F"],
#         "icon": "🌡️"
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping"],
#              "weights": {"Dry": 1, "Productive": 2, "Barking": 3, "Whooping": 4}},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1, "Nighttime": 2, "With feeding": 2, "After exercise": 2, "All day": 3}}
#         ],
#         "red_flags": ["Whooping sound on inspiration", "Cough causing vomiting"],
#         "icon": "🤧"
#     },
#     "RUNNY_NOSE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Nasal discharge with foul odor"],
#         "icon": "👃"
#     },
#     "SNEEZING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["Occasional", "Frequent", "Constant"],
#              "weights": {"Occasional": 1, "Frequent": 2, "Constant": 3}}
#         ],
#         "icon": "🤧"
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1, "5-8 loose stools/day": 2, ">8 loose stools/day": 3, "Watery": 3}},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1, "Mucoid": 2, "Bloody": 3, "Rice-water": 3}}
#         ],
#         "red_flags": ["Blood in stool", "Signs of dehydration"],
#         "icon": "💩"
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1, "No tears": 2, "Sunken eyes": 3, "Decreased urine output": 3, "Lethargy": 4}}
#         ],
#         "red_flags": ["Severe dehydration signs"],
#         "icon": "💧"
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3, "Doubled over": 4}}
#         ],
#         "red_flags": ["Severe localized pain", "Pain lasting >6 hours"],
#         "icon": "🤢"
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Macular", "Papular", "Vesicular", "Petechial/Purpuric"],
#              "weights": {"Macular": 1, "Papular": 2, "Vesicular": 3, "Petechial/Purpuric": 4}}
#         ],
#         "red_flags": ["Rash with fever", "Non-blanching rash"],
#         "icon": "🔴"
#     },
#     "HEADACHE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Severe headache with fever", "Headache with neck stiffness"],
#         "icon": "🤕"
#     }
# }

# # Find nearby doctors using Overpass API
# def find_nearby_doctors(lat, lon, radius=5000):
#     overpass_url = "https://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json];
#     (
#         node["amenity"="doctors"](around:{radius},{lat},{lon});
#         node["amenity"="clinic"](around:{radius},{lat},{lon});
#         node["healthcare"="doctor"](around:{radius},{lat},{lon});
#         node["healthcare"="pediatrician"](around:{radius},{lat},{lon});
#     );
#     out center;
#     """
#     try:
#         response = requests.get(overpass_url, params={'data': query})
#         response.raise_for_status()
#         data = response.json()
#         doctors = []
#         for element in data['elements']:
#             name = element.get('tags', {}).get('name', 'Unknown')
#             address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Address not available'))
#             specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
#             lat = element.get('lat', element.get('center', {}).get('lat'))
#             lon = element.get('lon', element.get('center', {}).get('lon'))
#             if lat and lon:
#                 doctors.append({'name': name, 'address': address, 'specialty': specialty, 'latitude': lat, 'longitude': lon})
#         return pd.DataFrame(doctors)
#     except Exception as e:
#         st.error(f"Error fetching nearby doctors: {e}")
#         return pd.DataFrame()

# # Show nearby doctors interface
# def show_nearby_doctors():
#     with st.expander("🚑 Find Nearby Pediatricians & Clinics", expanded=False):
#         st.markdown("### 🔍 Locate healthcare providers near you")
        
#         tab1, tab2 = st.tabs(["📍 Use Current Location", "🏠 Enter Address"])
        
#         with tab1:
#             st.info("We'll use your approximate location (no precise data is stored)")
#             if st.button("Detect My Location", key="detect_loc"):
#                 try:
#                     loc = st.experimental_get_query_params().get("location", None)
#                     if loc:
#                         lat, lon = map(float, loc[0].split(","))
#                         st.success(f"Location detected: {lat:.4f}, {lon:.4f}")
#                     else:
#                         st.warning("Couldn't detect location. Using default.")
#                         lat, lon = 40.7128, -74.0060
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     lat, lon = 40.7128, -74.0060
        
#         with tab2:
#             address = st.text_input("Enter your full address:", placeholder="e.g., 123 Main St, City, Country")
#             if address:
#                 geolocator = Nominatim(user_agent="pediatric-symptom-checker")
#                 try:
#                     location = geolocator.geocode(address)
#                     if location:
#                         lat, lon = location.latitude, location.longitude
#                         st.success(f"Found location: {lat:.4f}, {lon:.4f}")
#                     else:
#                         st.warning("Address not found. Using default.")
#                         lat, lon = 40.7128, -74.0060
#                 except Exception as e:
#                     st.error(f"Geocoding error: {e}")
#                     lat, lon = 40.7128, -74.0060
#             else:
#                 lat, lon = 40.7128, -74.0060
        
#         search_radius = st.slider("Search radius (meters)", 500, 10000, 2000, help="Wider radius may show more options")
        
#         if st.button("🔍 Search for Doctors", type="primary", use_container_width=True):
#             with st.spinner("Searching nearby..."):
#                 doctors_df = find_nearby_doctors(lat, lon, search_radius)
#                 if not doctors_df.empty:
#                     st.success(f"✅ Found {len(doctors_df)} healthcare providers nearby")
                    
#                     # Create map
#                     m = folium.Map(location=[lat, lon], zoom_start=13, tiles="cartodbpositron")
#                     folium.Marker(
#                         [lat, lon], 
#                         popup="Your Location", 
#                         icon=folium.Icon(color="blue", icon="user", prefix="fa")
#                     ).add_to(m)
                    
#                     # Add doctors
#                     for idx, row in doctors_df.iterrows():
#                         is_pediatric = "pediatric" in str(row['specialty']).lower()
#                         icon_color = "green" if is_pediatric else "red"
#                         icon_type = "child" if is_pediatric else "user-md"
                        
#                         folium.Marker(
#                             [row['latitude'], row['longitude']],
#                             popup=f"<b>{row['name']}</b><br><i>{row['specialty']}</i><br>{row['address']}",
#                             icon=folium.Icon(color=icon_color, icon=icon_type, prefix="fa")
#                         ).add_to(m)
                    
#                     # Display
#                     folium_static(m, width=700, height=500)
                    
#                     # Show table
#                     st.markdown("### 🏥 Nearby Healthcare Providers")
#                     st.dataframe(
#                         doctors_df[['name', 'specialty', 'address']].rename(columns={
#                             'name': 'Name',
#                             'specialty': 'Specialty',
#                             'address': 'Address'
#                         }),
#                         hide_index=True,
#                         use_container_width=True
#                     )
#                 else:
#                     st.warning("No doctors found in this area. Try increasing the search radius.")

# # Train the model
# @st.cache_resource
# def train_model(df):
#     df["AGE_FEATURE"] = 0
#     df["IMMUNOCOMPROMISED_FEATURE"] = 0
#     label_encoder = LabelEncoder()
#     df["CONDITION"] = label_encoder.fit_transform(df["CONDITION"])
#     X = df.drop(columns=["CONDITION"])
#     y = df["CONDITION"]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
#     pipeline = Pipeline([
#         ("scaler", StandardScaler()),
#         ("classifier", RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))
#     ])
#     pipeline.fit(X_train, y_train)
#     y_pred = pipeline.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     return pipeline, label_encoder

# # Step indicator component using Streamlit columns
# def show_step_indicator(current_step):
#     steps = [
#         {"title": "Patient Info", "number": 1},
#         {"title": "Select Symptoms", "number": 2},
#         {"title": "Symptom Details", "number": 3},
#         {"title": "Analysis", "number": 4}
#     ]
    
#     cols = st.columns(len(steps))
#     for i, step in enumerate(steps):
#         with cols[i]:
#             # Determine the step state
#             if step["number"] < current_step:
#                 step_state = "✅"  # Completed
#                 step_color = "#48dbb4"  # Success color
#             elif step["number"] == current_step:
#                 step_state = "➡️"  # Current
#                 step_color = "#4a6fa5"  # Primary color
#             else:
#                 step_state = str(step["number"])  # Not started
#                 step_color = "#e0e0e0"  # Gray
            
#             # Create a container for each step
#             st.markdown(
#                 f"""
#                 <div style="text-align: center; margin-bottom: 10px;">
#                     <div style="
#                         background-color: {step_color};
#                         color: white;
#                         width: 30px;
#                         height: 30px;
#                         border-radius: 50%;
#                         display: flex;
#                         align-items: center;
#                         justify-content: center;
#                         margin: 0 auto;
#                         font-weight: bold;
#                     ">{step_state}</div>
#                     <div style="font-weight: {'bold' if step['number'] == current_step else 'normal'};">
#                         {step['title']}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

# # Main application
# def main():
#     st.set_page_config(
#         page_title="Pediatric Symptom Checker", 
#         page_icon="👶", 
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )
#     local_css()
    
#     # Header with gradient
#     st.markdown("""
#     <div class="header-container">
#         <h1 style="margin:0;padding:0;">👶 Pediatric Symptom Checker</h1>
#         <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">A smart tool to help parents assess their child's symptoms and get guidance</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Introduction
#     st.markdown("""
#     <div class="card">
#         <p>Welcome to the Pediatric Symptom Checker. This tool helps you evaluate your child's symptoms and provides 
#         guidance on possible conditions. Please follow these steps:</p>
#         <ol>
#             <li>Provide basic information about your child</li>
#             <li>Select all symptoms your child is experiencing</li>
#             <li>Provide details about each symptom</li>
#             <li>Get an assessment with recommendations</li>
#         </ol>
#         <p><strong>Remember:</strong> This tool doesn't replace professional medical advice.</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Load data and model
#     file_path = "pages/pediatric_dataset_30k.csv"
#     df = load_data(file_path)
#     model, label_encoder = train_model(df)
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
#     # Step 1: Patient Information
#     with st.expander("👤 Step 1: Patient Information", expanded=True):
#         show_step_indicator(1)
#         st.markdown("### Tell us about your child")
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input(
#                 "Age (months)", 
#                 min_value=0, 
#                 max_value=216, 
#                 value=24, 
#                 step=1,
#                 help="Child's age in months (0-18 years)"
#             )
            
#             # Age category indicator
#             if age < 12:
#                 st.info("👶 Infant (0-12 months)")
#             elif age < 36:
#                 st.info("🧒 Toddler (1-3 years)")
#             elif age < 60:
#                 st.info("👦 Preschooler (3-5 years)")
#             else:
#                 st.info("👧 Child (5+ years)")
                
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                 default=[],
#                 help="Any pre-existing conditions"
#             )
            
#             if "Immunocompromised" in medical_history:
#                 st.warning("⚠️ Children with compromised immune systems may need special medical attention")
    
#     # Step 2: Symptom Selection
#     with st.expander("🤒 Step 2: Select Symptoms", expanded=False):
#         show_step_indicator(2)
#         st.markdown("### What symptoms is your child experiencing?")
        
#         # Symptom categories
#         tab1, tab2, tab3 = st.tabs(["🌡️ General Symptoms", "🤢 Digestive Symptoms", "🔴 Skin Symptoms"])
        
#         with tab1:
#             general_symptoms = ["FEVER", "COUGH", "RUNNY_NOSE", "SNEEZING", "HEADACHE"]
#             selected_general = st.multiselect(
#                 "General symptoms:",
#                 options=general_symptoms,
#                 format_func=lambda x: x.replace("_", " ").title(),
#                 placeholder="Select general symptoms...",
#                 key="general_symptoms"
#             )
        
#         with tab2:
#             digestive_symptoms = ["DIARRHEA", "DEHYDRATION", "ABDOMINAL_PAIN"]
#             selected_digestive = st.multiselect(
#                 "Digestive symptoms:",
#                 options=digestive_symptoms,
#                 format_func=lambda x: x.replace("_", " ").title(),
#                 placeholder="Select digestive symptoms...",
#                 key="digestive_symptoms"
#             )
        
#         with tab3:
#             skin_symptoms = ["RASH"]
#             selected_skin = st.multiselect(
#                 "Skin symptoms:",
#                 options=skin_symptoms,
#                 format_func=lambda x: x.replace("_", " ").title(),
#                 placeholder="Select skin symptoms...",
#                 key="skin_symptoms"
#             )
        
#         primary_symptoms = selected_general + selected_digestive + selected_skin
        
#         if primary_symptoms:
#             st.markdown(f"<div class='info-card'>Selected symptoms: {', '.join([s.replace('_', ' ').title() for s in primary_symptoms])}</div>", unsafe_allow_html=True)
    
#     # Step 3: Symptom Details
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("📝 Step 3: Symptom Details", expanded=False):
#             show_step_indicator(3)
#             st.markdown("### Provide more details about each symptom")
#             progress_bar = st.progress(0)
#             total_symptoms = len(primary_symptoms)
            
#             for i, symptom in enumerate(primary_symptoms):
#                 with st.container():
#                     icon = SYMPTOM_DEFINITIONS.get(symptom, {}).get("icon", "ℹ️")
#                     st.markdown(f"<div class='symptom-card'><h4>{icon} {symptom.replace('_', ' ').title()}</h4></div>", unsafe_allow_html=True)
                    
#                     if symptom in SYMPTOM_DEFINITIONS:
#                         symptom_score = 0
#                         for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                             if question["type"] == "radio":
#                                 response = st.radio(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}",
#                                     horizontal=True
#                                 )
#                                 symptom_score += question["weights"][response]
#                             elif question["type"] == "selectbox":
#                                 response = st.selectbox(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}"
#                                 )
#                                 symptom_score += question["weights"][response]
#                             elif question["type"] == "checkbox":
#                                 response = st.multiselect(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}"
#                                 )
#                                 for item in response:
#                                     symptom_score += question["weights"][item]
#                         symptom_details[symptom] = symptom_score
#                     else:
#                         severity = st.slider(
#                             f"Severity of {symptom.replace('_', ' ')}",
#                             min_value=0.1, 
#                             max_value=3.0, 
#                             value=1.0, 
#                             step=0.1, 
#                             key=symptom,
#                             help="1 = Mild, 3 = Severe"
#                         )
#                         symptom_details[symptom] = severity
                    
#                     progress_bar.progress((i + 1) / total_symptoms)
#                     if i < total_symptoms - 1:
#                         st.divider()
    
#     # Step 4: Analysis
#     show_step_indicator(4 if primary_symptoms else 3)
#     if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             st.stop()
        
#         with st.spinner("Analyzing symptoms..."):
#             # Add a slight delay for better UX
#             time.sleep(1)
            
#             # Prepare input features
#             input_features = {col: 0.0 for col in all_symptoms}
#             input_features["AGE_FEATURE"] = 3 if age < 3 else (2 if age < 12 else 1)
#             input_features["IMMUNOCOMPROMISED_FEATURE"] = 1 if "Immunocompromised" in medical_history else 0
            
#             for symptom, score in symptom_details.items():
#                 if symptom in input_features:
#                     input_features[symptom] = score
            
#             # Make prediction
#             input_df = pd.DataFrame([input_features])
#             prediction = model.predict(input_df)[0]
#             probabilities = model.predict_proba(input_df)[0]
#             prediction = label_encoder.inverse_transform([prediction])[0]
            
#             # Get red flags
#             red_flags = []
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])
            
#             # Generate recommendations
#             recommendations = []
#             if "Meningitis" in prediction:
#                 recommendations.append("EMERGENCY: Seek immediate medical attention - This is a medical emergency requiring IV antibiotics.")
#             if "Immunocompromised" in medical_history:
#                 recommendations.append("Children with compromised immune systems should be evaluated earlier for infections.")
#             if "FEVER" in primary_symptoms and age < 3:
#                 recommendations.append("Infants under 3 months with fever should be evaluated by a doctor immediately.")
#             if "DEHYDRATION" in primary_symptoms:
#                 recommendations.append("Ensure adequate fluid intake and monitor for worsening signs of dehydration.")
            
#             # Display results
#             st.markdown("---")
#             st.markdown(f"""
#             <div class='diagnosis-highlight'>
#                 <h2 style='text-align:center;margin-bottom:0.5rem;'>Diagnostic Results</h2>
#                 <h3 style='text-align:center;color:#4a6fa5;margin-top:0;'>Most likely condition: {prediction}</h3>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Condition probabilities
#             st.markdown("### Condition Probabilities")
#             prob_df = pd.DataFrame({
#                 "Condition": label_encoder.classes_,
#                 "Probability": probabilities
#             }).sort_values("Probability", ascending=False)
            
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"}),
#                 column_config={
#                     "Condition": "Possible Condition",
#                     "Probability": st.column_config.ProgressColumn(
#                         "Probability",
#                         help="How likely this condition is",
#                         format="%.2f%%",
#                         min_value=0,
#                         max_value=1,
#                     )
#                 },
#                 hide_index=True,
#                 use_container_width=True
#             )
            
#             # Red flags
#             if red_flags:
#                 st.markdown("### ⚠️ Red Flags")
#                 for flag in red_flags:
#                     st.markdown(f"""
#                     <div class='red-flag'>
#                         <p style='margin:0;'><strong>{flag}</strong></p>
#                     </div>
#                     """, unsafe_allow_html=True)
#             else:
#                 st.markdown("""
#                 <div class='card' style='background-color:#e8f5e9;'>
#                     <h4 style='color:#2e7d32;margin:0;'>No urgent red flags identified</h4>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # Recommendations
#             if recommendations:
#                 st.markdown("### Recommended Actions")
#                 for rec in recommendations:
#                     st.markdown(f"""
#                     <div class='recommendation'>
#                         <p style='margin:0;'>{rec}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
            
#             # Additional advice based on condition
#             st.markdown("### ℹ️ Additional Information")
#             if "Common Cold" in prediction:
#                 st.markdown("""
#                 <div class='info-card'>
#                     <p><strong>For common cold:</strong></p>
#                     <ul>
#                         <li>Ensure your child gets plenty of rest</li>
#                         <li>Use saline nasal drops to relieve congestion</li>
#                         <li>Offer warm fluids to soothe throat irritation</li>
#                         <li>Use a cool-mist humidifier in the room</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)
#             elif "Gastroenteritis" in prediction:
#                 st.markdown("""
#                 <div class='info-card'>
#                     <p><strong>For gastroenteritis:</strong></p>
#                     <ul>
#                         <li>Offer small, frequent amounts of oral rehydration solution</li>
#                         <li>Avoid sugary drinks and dairy products</li>
#                         <li>Gradually reintroduce bland foods (BRAT diet: bananas, rice, applesauce, toast)</li>
#                         <li>Watch for signs of dehydration</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # PDF Report
#             st.markdown("---")
#             st.markdown("### 📄 Download Report")
#             pdf = generate_pdf_report(
#                 patient_info={"age": age, "medical_history": medical_history},
#                 symptoms=symptom_details,
#                 prediction=prediction,
#                 probabilities_df=prob_df,
#                 red_flags=red_flags,
#                 recommendations=recommendations
#             )
            
#             pdf_output = pdf.output(dest='S').encode('latin-1')
#             b64 = base64.b64encode(pdf_output).decode()
#             href = f"""
#             <a href="data:application/octet-stream;base64,{b64}" download="pediatric_health_report.pdf" style='
#                 display: inline-block;
#                 background-color: #4a6fa5;
#                 color: white;
#                 padding: 12px 24px;
#                 text-align: center;
#                 text-decoration: none;
#                 font-size: 16px;
#                 margin: 4px 2px;
#                 cursor: pointer;
#                 border-radius: 8px;
#                 border: none;
#                 transition: all 0.3s ease;
#             ' onmouseover="this.style.backgroundColor='#166088'" onmouseout="this.style.backgroundColor='#4a6fa5'">📥 Download Full Medical Report</a>
#             """
#             st.markdown(href, unsafe_allow_html=True)
    
#     # Nearby doctors section
#     st.markdown("---")
#     show_nearby_doctors()
    
#     # # Feedback section
#     # with st.expander("💬 Provide Feedback", expanded=False):
#     #     st.markdown("### Help us improve this tool")
#     #     feedback = st.text_area("Your feedback (optional):", placeholder="What did you like or what could be improved?")
#     #     if st.button("Submit Feedback", type="secondary"):
#     #         st.success("Thank you for your feedback! We appreciate your input.")
    
#     # Footer
#     st.markdown("""
#     <div class="footer">
#         <p>This tool is for informational purposes only and does not provide medical advice.</p>
#         <p>Always consult a qualified healthcare provider for diagnosis and treatment.</p>
#         <p style="font-size:0.8em;margin-top:1rem;">Version 1.1.0 | Last updated: {date}</p>
#     </div>
#     """.format(date=datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

#old categories


# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.pipeline import Pipeline
# import requests
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# from fpdf import FPDF
# import base64
# from datetime import datetime
# import time
# import random

# # Custom CSS for modern UI
# def local_css():
#     st.markdown("""
#     <style>
#         :root {
#             --primary: #4a6fa5;
#             --secondary: #166088;
#             --accent: #4fc1e9;
#             --background: #f8f9fa;
#             --card: #ffffff;
#             --text: #2c3e50;
#             --warning: #ff6b6b;
#             --success: #48dbb4;
#             --info: #5bc0de;
#         }
        
#         .main {
#             background-color: var(--background);
#         }
        
#         /* Header styling */
#         .header-container {
#             background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
#             padding: 2rem;
#             border-radius: 12px;
#             margin-bottom: 2rem;
#             box-shadow: 0 4px 20px rgba(0,0,0,0.1);
#             color: white;
#             text-align: center;
#         }
        
#         /* Button styling */
#         .stButton>button {
#             background-color: var(--primary);
#             color: white;
#             border-radius: 8px;
#             padding: 0.75rem 1.5rem;
#             font-weight: 600;
#             border: none;
#             transition: all 0.3s ease;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#         }
        
#         .stButton>button:hover {
#             background-color: var(--secondary);
#             transform: translateY(-2px);
#             box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#         }
        
#         .stButton>button:active {
#             transform: translateY(0);
#         }
        
#         /* Primary button */
#         .primary-button {
#             background-color: var(--primary) !important;
#             color: white !important;
#         }
        
#         /* Secondary button */
#         .secondary-button {
#             background-color: var(--secondary) !important;
#             color: white !important;
#         }
        
#         /* Progress bar */
#         .stProgress > div > div > div > div {
#             background-color: var(--accent);
#         }
        
#         /* Cards */
#         .card {
#             background-color: var(--card);
#             border-radius: 12px;
#             padding: 1.5rem;
#             margin-bottom: 1rem;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#             border: 1px solid rgba(0,0,0,0.05);
#         }
        
#         /* Expander styling */
#         .streamlit-expanderHeader {
#             font-weight: 600;
#             color: var(--primary);
#             font-size: 1.1rem;
#         }
        
#         .streamlit-expanderContent {
#             padding: 1rem 1.5rem;
#         }
        
#         /* Alert boxes */
#         .stAlert {
#             border-radius: 12px;
#         }
        
#         /* Custom components */
#         .symptom-card {
#             background-color: var(--card);
#             border-radius: 12px;
#             padding: 1.25rem;
#             margin-bottom: 1rem;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.05);
#             transition: all 0.3s ease;
#             border-left: 4px solid var(--accent);
#         }
        
#         .symptom-card:hover {
#             box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#             transform: translateY(-2px);
#         }
        
#         .red-flag {
#             background-color: rgba(255,107,107,0.1);
#             border-left: 4px solid var(--warning);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#             animation: pulse 2s infinite;
#         }
        
#         .recommendation {
#             background-color: rgba(72,219,180,0.1);
#             border-left: 4px solid var(--success);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#         }
        
#         .info-card {
#             background-color: rgba(91,192,222,0.1);
#             border-left: 4px solid var(--info);
#             padding: 1rem;
#             margin: 0.5rem 0;
#             border-radius: 0 8px 8px 0;
#         }
        
#         .diagnosis-highlight {
#             background: linear-gradient(135deg, rgba(74,111,165,0.1) 0%, rgba(22,96,136,0.1) 100%);
#             padding: 1.5rem;
#             border-radius: 12px;
#             margin-bottom: 1.5rem;
#             border: 1px solid rgba(74,111,165,0.2);
#         }
        
#         @keyframes pulse {
#             0% { box-shadow: 0 0 0 0 rgba(255,107,107,0.4); }
#             70% { box-shadow: 0 0 0 10px rgba(255,107,107,0); }
#             100% { box-shadow: 0 0 0 0 rgba(255,107,107,0); }
#         }
        
#         /* Tabs */
#         .stTabs [data-baseweb="tab-list"] {
#             gap: 10px;
#         }
        
#         .stTabs [data-baseweb="tab"] {
#             height: 50px;
#             padding: 0 20px;
#             background-color: #f0f4f8;
#             border-radius: 8px 8px 0 0 !important;
#             font-weight: 500;
#             transition: all 0.2s ease;
#         }
        
#         .stTabs [data-baseweb="tab"]:hover {
#             background-color: #e1e8f0;
#         }
        
#         .stTabs [aria-selected="true"] {
#             background-color: var(--primary) !important;
#             color: white !important;
#         }
        
#         /* Input fields */
#         .stTextInput input, .stNumberInput input, .stSelectbox select {
#             border-radius: 8px !important;
#             padding: 10px 12px !important;
#         }
        
#         /* Radio buttons */
#         .stRadio [role="radiogroup"] {
#             gap: 15px;
#         }
        
#         .stRadio [role="radio"] {
#             padding: 8px 16px;
#             border-radius: 8px;
#             border: 1px solid #dfe3e8;
#         }
        
#         .stRadio [role="radio"][aria-checked="true"] {
#             background-color: var(--primary);
#             color: white;
#             border-color: var(--primary);
#         }
        
#         /* Sliders */
#         .stSlider [role="slider"] {
#             background-color: var(--primary) !important;
#         }
        
#         /* Footer */
#         .footer {
#             text-align: center;
#             padding: 1.5rem;
#             color: #666;
#             font-size: 0.9em;
#             margin-top: 2rem;
#             border-top: 1px solid #eee;
#         }
        
#         /* Tooltips */
#         .stTooltip {
#             border-radius: 8px !important;
#             padding: 8px 12px !important;
#         }
        
#         /* Responsive adjustments */
#         @media (max-width: 768px) {
#             .header-container {
#                 padding: 1.5rem 1rem;
#             }
            
#             .stButton>button {
#                 padding: 0.5rem 1rem;
#             }
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # PDF Report Generator
# def generate_pdf_report(patient_info, symptoms, prediction, probabilities_df, red_flags, recommendations):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", 'B', 16)
    
#     # Header with color
#     pdf.set_fill_color(74, 111, 165)
#     pdf.set_text_color(255, 255, 255)
#     pdf.cell(0, 10, "Pediatric Health Report", 0, 1, 'C', 1)
#     pdf.set_font("Arial", '', 10)
#     pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C', 1)
#     pdf.ln(10)
    
#     # Reset colors
#     pdf.set_fill_color(255, 255, 255)
#     pdf.set_text_color(0, 0, 0)
    
#     # Patient Information
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Patient Information", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     pdf.cell(0, 8, f"Age: {patient_info['age']} months", 0, 1)
#     pdf.cell(0, 8, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", 0, 1)
#     pdf.ln(5)
    
#     # Symptoms
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Reported Symptoms", 0, 1)
#     pdf.set_font("Arial", '', 12)
#     for symptom, details in symptoms.items():
#         pdf.cell(0, 8, f"- {symptom.replace('_', ' ').title()}: Severity score {details}", 0, 1)
#     pdf.ln(5)
    
#     # Diagnosis
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Diagnostic Assessment", 0, 1)
#     pdf.set_font("Arial", 'B', 12)
#     pdf.set_text_color(74, 111, 165)  # Primary color
#     pdf.cell(0, 8, f"Most Likely Condition: {prediction}", 0, 1)
#     pdf.set_text_color(0, 0, 0)
#     pdf.set_font("Arial", '', 12)
    
#     # Probability table
#     pdf.cell(0, 8, "Condition Probabilities:", 0, 1)
#     col_width = pdf.w / 3
#     pdf.set_font("Arial", 'B', 12)
#     pdf.cell(col_width, 8, "Condition", 1)
#     pdf.cell(col_width, 8, "Probability", 1, 1)
#     pdf.set_font("Arial", '', 12)
    
#     for _, row in probabilities_df.iterrows():
#         pdf.cell(col_width, 8, row['Condition'], 1)
#         pdf.cell(col_width, 8, f"{row['Probability']:.2%}", 1, 1)
#     pdf.ln(5)
    
#     # Red Flags
#     if red_flags:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.set_text_color(255, 107, 107)  # Warning color
#         pdf.cell(0, 10, "Red Flags", 0, 1)
#         pdf.set_text_color(0, 0, 0)
#         pdf.set_font("Arial", '', 12)
#         for flag in red_flags:
#             pdf.cell(0, 8, f"- {flag}", 0, 1)
#         pdf.ln(5)
    
#     # Recommendations
#     if recommendations:
#         pdf.set_font("Arial", 'B', 14)
#         pdf.set_text_color(72, 219, 180)  # Success color
#         pdf.cell(0, 10, "Recommendations", 0, 1)
#         pdf.set_text_color(0, 0, 0)
#         pdf.set_font("Arial", '', 12)
#         for rec in recommendations:
#             pdf.cell(0, 8, f"- {rec}", 0, 1)
#         pdf.ln(5)
    
#     # Disclaimer
#     pdf.set_font("Arial", 'I', 10)
#     pdf.multi_cell(0, 8, "Disclaimer: This report is generated by an AI system and should not replace professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
    
#     return pdf

# # Load and preprocess the dataset
# @st.cache_data
# def load_data(file_path):
#     df = pd.read_csv(file_path)
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# # Enhanced medical knowledge base with all symptoms from the dataset
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio",
#              "options": ["<100.4°F", "100.4-102.2°F", "102.2-104°F", ">104°F"],
#              "weights": {"<100.4°F": 1, "100.4-102.2°F": 2, "102.2-104°F": 3, ">104°F": 4}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 1, "1-3 days": 2, "3-7 days": 3, ">7 days": 4}}
#         ],
#         "red_flags": ["Fever >100.4°F in infants <3 months", "Fever >104°F"],
#         "icon": "🌡️"
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping"],
#              "weights": {"Dry": 1, "Productive": 2, "Barking": 3, "Whooping": 4}},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1, "Nighttime": 2, "With feeding": 2, "After exercise": 2, "All day": 3}}
#         ],
#         "red_flags": ["Whooping sound on inspiration", "Cough causing vomiting"],
#         "icon": "🤧"
#     },
#     "RUNNY_NOSE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Nasal discharge with foul odor"],
#         "icon": "👃"
#     },
#     "SNEEZING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["Occasional", "Frequent", "Constant"],
#              "weights": {"Occasional": 1, "Frequent": 2, "Constant": 3}}
#         ],
#         "icon": "🤧"
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1, "5-8 loose stools/day": 2, ">8 loose stools/day": 3, "Watery": 3}},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1, "Mucoid": 2, "Bloody": 3, "Rice-water": 3}}
#         ],
#         "red_flags": ["Blood in stool", "Signs of dehydration"],
#         "icon": "💩"
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1, "No tears": 2, "Sunken eyes": 3, "Decreased urine output": 3, "Lethargy": 4}}
#         ],
#         "red_flags": ["Severe dehydration signs"],
#         "icon": "💧"
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3, "Doubled over": 4}},
#             {"question": "Location", "type": "selectbox",
#              "options": ["Generalized", "Upper abdomen", "Lower abdomen", "Right side", "Left side"],
#              "weights": {"Generalized": 1, "Upper abdomen": 2, "Lower abdomen": 2, "Right side": 3, "Left side": 3}}
#         ],
#         "red_flags": ["Severe localized pain", "Pain lasting >6 hours"],
#         "icon": "🤢"
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Macular", "Papular", "Vesicular", "Petechial/Purpuric"],
#              "weights": {"Macular": 1, "Papular": 2, "Vesicular": 3, "Petechial/Purpuric": 4}},
#             {"question": "Distribution", "type": "checkbox",
#              "options": ["Face", "Trunk", "Extremities", "Palms/Soles", "Generalized"],
#              "weights": {"Face": 1, "Trunk": 1, "Extremities": 1, "Palms/Soles": 2, "Generalized": 2}}
#         ],
#         "red_flags": ["Rash with fever", "Non-blanching rash"],
#         "icon": "🔴"
#     },
#     "HEADACHE": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<1 hour", "1-4 hours", "4-24 hours", ">24 hours"],
#              "weights": {"<1 hour": 1, "1-4 hours": 2, "4-24 hours": 3, ">24 hours": 4}}
#         ],
#         "red_flags": ["Severe headache with fever", "Headache with neck stiffness"],
#         "icon": "🤕"
#     },
#     "CHEST_PAIN": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Sharp", "Dull", "Burning", "Pressure"],
#              "weights": {"Sharp": 1, "Dull": 2, "Burning": 2, "Pressure": 3}},
#             {"question": "Associated Symptoms", "type": "checkbox",
#              "options": ["Shortness of breath", "Palpitations", "Cough", "Fever"],
#              "weights": {"Shortness of breath": 2, "Palpitations": 2, "Cough": 1, "Fever": 1}}
#         ],
#         "red_flags": ["Chest pain with shortness of breath", "Chest pain with palpitations"],
#         "icon": "💔"
#     },
#     "ITCHING": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Location", "type": "checkbox",
#              "options": ["Face", "Trunk", "Extremities", "Generalized"],
#              "weights": {"Face": 1, "Trunk": 1, "Extremities": 1, "Generalized": 2}}
#         ],
#         "icon": "🦠"
#     },
#     "MUSCLE_ACHES": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", ">3 days"],
#              "weights": {"<24 hours": 1, "1-3 days": 2, ">3 days": 3}}
#         ],
#         "icon": "💪"
#     },
#     "NAUSEA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Associated Symptoms", "type": "checkbox",
#              "options": ["Vomiting", "Dizziness", "Headache", "Fever"],
#              "weights": {"Vomiting": 2, "Dizziness": 1, "Headache": 1, "Fever": 1}}
#         ],
#         "icon": "🤢"
#     },
#     "NECK_STIFFNESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Associated Symptoms", "type": "checkbox",
#              "options": ["Fever", "Headache", "Photophobia"],
#              "weights": {"Fever": 3, "Headache": 2, "Photophobia": 2}}
#         ],
#         "red_flags": ["Neck stiffness with fever"],
#         "icon": "🦴"
#     },
#     "PHOTOPHOBIA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "red_flags": ["Photophobia with headache and fever"],
#         "icon": "👁️"
#     },
#     "POLYDIPSIA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "icon": "🚰"
#     },
#     "POLYURIA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
#         ],
#         "icon": "🚽"
#     },
#     "RESPIRATORY_DISTRESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Nasal flaring", "Retractions", "Grunting", "Cyanosis"],
#              "weights": {"Nasal flaring": 2, "Retractions": 3, "Grunting": 3, "Cyanosis": 4}}
#         ],
#         "red_flags": ["Respiratory distress with cyanosis"],
#         "icon": "😮‍💨"
#     },
#     "SORE_THROAT": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", ">3 days"],
#              "weights": {"<24 hours": 1, "1-3 days": 2, ">3 days": 3}}
#         ],
#         "icon": "👄"
#     },
#     "STRIDOR": {
#         "follow_up": [
#             {"question": "Timing", "type": "radio",
#              "options": ["Inspiratory", "Expiratory", "Both"],
#              "weights": {"Inspiratory": 2, "Expiratory": 3, "Both": 4}}
#         ],
#         "red_flags": ["Stridor at rest"],
#         "icon": "🎵"
#     },
#     "VOMITING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["1-2 times", "3-5 times", ">5 times"],
#              "weights": {"1-2 times": 1, "3-5 times": 2, ">5 times": 3}},
#             {"question": "Content", "type": "selectbox",
#              "options": ["Food", "Bile", "Blood"],
#              "weights": {"Food": 1, "Bile": 2, "Blood": 3}}
#         ],
#         "red_flags": ["Projectile vomiting", "Vomiting blood"],
#         "icon": "🤮"
#     },
#     "WEIGHT_LOSS": {
#         "follow_up": [
#             {"question": "Amount", "type": "radio",
#              "options": ["<5% body weight", "5-10% body weight", ">10% body weight"],
#              "weights": {"<5% body weight": 1, "5-10% body weight": 2, ">10% body weight": 3}},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<1 week", "1-4 weeks", ">4 weeks"],
#              "weights": {"<1 week": 1, "1-4 weeks": 2, ">4 weeks": 3}}
#         ],
#         "red_flags": ["Rapid weight loss"],
#         "icon": "⚖️"
#     },
#     "WHEEZING": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
#             {"question": "Timing", "type": "selectbox",
#              "options": ["Occasional", "With activity", "At rest"],
#              "weights": {"Occasional": 1, "With activity": 2, "At rest": 3}}
#         ],
#         "red_flags": ["Wheezing at rest"],
#         "icon": "🎵"
#     }
# }

# # Find nearby doctors using Overpass API
# def find_nearby_doctors(lat, lon, radius=5000):
#     overpass_url = "https://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json];
#     (
#         node["amenity"="doctors"](around:{radius},{lat},{lon});
#         node["amenity"="clinic"](around:{radius},{lat},{lon});
#         node["healthcare"="doctor"](around:{radius},{lat},{lon});
#         node["healthcare"="pediatrician"](around:{radius},{lat},{lon});
#     );
#     out center;
#     """
#     try:
#         response = requests.get(overpass_url, params={'data': query})
#         response.raise_for_status()
#         data = response.json()
#         doctors = []
#         for element in data['elements']:
#             name = element.get('tags', {}).get('name', 'Unknown')
#             address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Address not available'))
#             specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
#             lat = element.get('lat', element.get('center', {}).get('lat'))
#             lon = element.get('lon', element.get('center', {}).get('lon'))
#             if lat and lon:
#                 doctors.append({'name': name, 'address': address, 'specialty': specialty, 'latitude': lat, 'longitude': lon})
#         return pd.DataFrame(doctors)
#     except Exception as e:
#         st.error(f"Error fetching nearby doctors: {e}")
#         return pd.DataFrame()

# # Show nearby doctors interface
# def show_nearby_doctors():
#     with st.expander("🚑 Find Nearby Pediatricians & Clinics", expanded=False):
#         st.markdown("### 🔍 Locate healthcare providers near you")
        
#         tab1, tab2 = st.tabs(["📍 Use Current Location", "🏠 Enter Address"])
        
#         with tab1:
#             st.info("We'll use your approximate location (no precise data is stored)")
#             if st.button("Detect My Location", key="detect_loc"):
#                 try:
#                     loc = st.experimental_get_query_params().get("location", None)
#                     if loc:
#                         lat, lon = map(float, loc[0].split(","))
#                         st.success(f"Location detected: {lat:.4f}, {lon:.4f}")
#                     else:
#                         st.warning("Couldn't detect location. Using default.")
#                         lat, lon = 40.7128, -74.0060
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     lat, lon = 40.7128, -74.0060
        
#         with tab2:
#             address = st.text_input("Enter your full address:", placeholder="e.g., 123 Main St, City, Country")
#             if address:
#                 geolocator = Nominatim(user_agent="pediatric-symptom-checker")
#                 try:
#                     location = geolocator.geocode(address)
#                     if location:
#                         lat, lon = location.latitude, location.longitude
#                         st.success(f"Found location: {lat:.4f}, {lon:.4f}")
#                     else:
#                         st.warning("Address not found. Using default.")
#                         lat, lon = 40.7128, -74.0060
#                 except Exception as e:
#                     st.error(f"Geocoding error: {e}")
#                     lat, lon = 40.7128, -74.0060
#             else:
#                 lat, lon = 40.7128, -74.0060
        
#         search_radius = st.slider("Search radius (meters)", 500, 10000, 2000, help="Wider radius may show more options")
        
#         if st.button("🔍 Search for Doctors", type="primary", use_container_width=True):
#             with st.spinner("Searching nearby..."):
#                 doctors_df = find_nearby_doctors(lat, lon, search_radius)
#                 if not doctors_df.empty:
#                     st.success(f"✅ Found {len(doctors_df)} healthcare providers nearby")
                    
#                     # Create map
#                     m = folium.Map(location=[lat, lon], zoom_start=13, tiles="cartodbpositron")
#                     folium.Marker(
#                         [lat, lon], 
#                         popup="Your Location", 
#                         icon=folium.Icon(color="blue", icon="user", prefix="fa")
#                     ).add_to(m)
                    
#                     # Add doctors
#                     for idx, row in doctors_df.iterrows():
#                         is_pediatric = "pediatric" in str(row['specialty']).lower()
#                         icon_color = "green" if is_pediatric else "red"
#                         icon_type = "child" if is_pediatric else "user-md"
                        
#                         folium.Marker(
#                             [row['latitude'], row['longitude']],
#                             popup=f"<b>{row['name']}</b><br><i>{row['specialty']}</i><br>{row['address']}",
#                             icon=folium.Icon(color=icon_color, icon=icon_type, prefix="fa")
#                         ).add_to(m)
                    
#                     # Display
#                     folium_static(m, width=700, height=500)
                    
#                     # Show table
#                     st.markdown("### 🏥 Nearby Healthcare Providers")
#                     st.dataframe(
#                         doctors_df[['name', 'specialty', 'address']].rename(columns={
#                             'name': 'Name',
#                             'specialty': 'Specialty',
#                             'address': 'Address'
#                         }),
#                         hide_index=True,
#                         use_container_width=True
#                     )
#                 else:
#                     st.warning("No doctors found in this area. Try increasing the search radius.")

# # Train the model
# @st.cache_resource
# def train_model(df):
#     df["AGE_FEATURE"] = 0
#     df["IMMUNOCOMPROMISED_FEATURE"] = 0
#     label_encoder = LabelEncoder()
#     df["CONDITION"] = label_encoder.fit_transform(df["CONDITION"])
#     X = df.drop(columns=["CONDITION"])
#     y = df["CONDITION"]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
#     pipeline = Pipeline([
#         ("scaler", StandardScaler()),
#         ("classifier", RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))
#     ])
#     pipeline.fit(X_train, y_train)
#     y_pred = pipeline.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     return pipeline, label_encoder

# # Step indicator component using Streamlit columns
# def show_step_indicator(current_step):
#     steps = [
#         {"title": "Patient Info", "number": 1},
#         {"title": "Select Symptoms", "number": 2},
#         {"title": "Symptom Details", "number": 3},
#         {"title": "Analysis", "number": 4}
#     ]
    
#     cols = st.columns(len(steps))
#     for i, step in enumerate(steps):
#         with cols[i]:
#             # Determine the step state
#             if step["number"] < current_step:
#                 step_state = "✅"  # Completed
#                 step_color = "#48dbb4"  # Success color
#             elif step["number"] == current_step:
#                 step_state = "➡️"  # Current
#                 step_color = "#4a6fa5"  # Primary color
#             else:
#                 step_state = str(step["number"])  # Not started
#                 step_color = "#e0e0e0"  # Gray
            
#             # Create a container for each step
#             st.markdown(
#                 f"""
#                 <div style="text-align: center; margin-bottom: 10px;">
#                     <div style="
#                         background-color: {step_color};
#                         color: white;
#                         width: 30px;
#                         height: 30px;
#                         border-radius: 50%;
#                         display: flex;
#                         align-items: center;
#                         justify-content: center;
#                         margin: 0 auto;
#                         font-weight: bold;
#                     ">{step_state}</div>
#                     <div style="font-weight: {'bold' if step['number'] == current_step else 'normal'};">
#                         {step['title']}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

# # Main application
# def main():
#     st.set_page_config(
#         page_title="Pediatric Symptom Checker", 
#         page_icon="👶", 
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )
#     local_css()
    
#     # Header with gradient
#     st.markdown("""
#     <div class="header-container">
#         <h1 style="margin:0;padding:0;">👶 Pediatric Symptom Checker</h1>
#         <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">A smart tool to help parents assess their child's symptoms and get guidance</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Introduction
#     st.markdown("""
#     <div class="card">
#         <p>Welcome to the Pediatric Symptom Checker. This tool helps you evaluate your child's symptoms and provides 
#         guidance on possible conditions. Please follow these steps:</p>
#         <ol>
#             <li>Provide basic information about your child</li>
#             <li>Select all symptoms your child is experiencing</li>
#             <li>Provide details about each symptom</li>
#             <li>Get an assessment with recommendations</li>
#         </ol>
#         <p><strong>Remember:</strong> This tool doesn't replace professional medical advice.</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Load data and model
#     file_path = "pages/pediatric_dataset_30k.csv"
#     df = load_data(file_path)
#     model, label_encoder = train_model(df)
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
#     # Step 1: Patient Information
#     with st.expander("👤 Step 1: Patient Information", expanded=True):
#         show_step_indicator(1)
#         st.markdown("### Tell us about your child")
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input(
#                 "Age (months)", 
#                 min_value=0, 
#                 max_value=216, 
#                 value=24, 
#                 step=1,
#                 help="Child's age in months (0-18 years)"
#             )
            
#             # Age category indicator
#             if age < 12:
#                 st.info("👶 Infant (0-12 months)")
#             elif age < 36:
#                 st.info("🧒 Toddler (1-3 years)")
#             elif age < 60:
#                 st.info("👦 Preschooler (3-5 years)")
#             else:
#                 st.info("👧 Child (5+ years)")
                
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Allergies (Food, Environmental, Medication)", "Asthma", 
#                          "Immunocompromised Status", "Prematurity or Neonatal Complications"],
#                 default=[]
#             )
#              # Set red flags based on medical history and age
#             red_flags = []
#             if "Immunocompromised Status" in medical_history:
#                 red_flags.append("Caution: Child with immunocompromised status.")
#             if (age < 12) and ("Asthma" in medical_history):
#                 red_flags.append("Caution: Children with asthma are more vulnerable.")
#             if (age < 3) and ("Allergies (Food, Environmental, Medication)" in medical_history):
#                 red_flags.append("Caution: Allergies may be more dangerous in infants.")
            
#             # if "Immunocompromised" in medical_history:
#             #     st.warning("⚠️ Children with compromised immune systems may need special medical attention")
    
#     # Step 2: Symptom Selection
#     with st.expander("🤒 Step 2: Select Symptoms", expanded=False):
#         show_step_indicator(2)
#         st.markdown("### What symptoms is your child experiencing?")
        
#         # Symptom categories
#         tab1, tab2, tab3 = st.tabs(["🌡️ General Symptoms", "🤢 Digestive Symptoms", "🔴 Skin Symptoms"])
        
#         with tab1:
#             general_symptoms = ["FEVER", "COUGH", "RUNNY_NOSE", "SNEEZING", "HEADACHE", "CHEST_PAIN", "MUSCLE_ACHES", "NECK_STIFFNESS", "PHOTOPHOBIA", "RESPIRATORY_DISTRESS", "SORE_THROAT", "STRIDOR", "WHEEZING"]
#             selected_general = st.multiselect(
#                 "General symptoms:",
#                 options=general_symptoms,
#                 format_func=lambda x: x.replace("_", " ").title(),
#                 placeholder="Select general symptoms...",
#                 key="general_symptoms"
#             )
        
#         with tab2:
#             digestive_symptoms = ["DIARRHEA", "DEHYDRATION", "ABDOMINAL_PAIN", "NAUSEA", "VOMITING", "POLYDIPSIA", "POLYURIA", "WEIGHT_LOSS"]
#             selected_digestive = st.multiselect(
#                 "Digestive symptoms:",
#                 options=digestive_symptoms,
#                 format_func=lambda x: x.replace("_", " ").title(),
#                 placeholder="Select digestive symptoms...",
#                 key="digestive_symptoms"
#             )
        
#         with tab3:
#             skin_symptoms = ["RASH", "ITCHING"]
#             selected_skin = st.multiselect(
#                 "Skin symptoms:",
#                 options=skin_symptoms,
#                 format_func=lambda x: x.replace("_", " ").title(),
#                 placeholder="Select skin symptoms...",
#                 key="skin_symptoms"
#             )
            
        
#         primary_symptoms = selected_general + selected_digestive + selected_skin
        
#         if primary_symptoms:
#             st.markdown(f"<div class='info-card'>Selected symptoms: {', '.join([s.replace('_', ' ').title() for s in primary_symptoms])}</div>", unsafe_allow_html=True)
    
#     # Step 3: Symptom Details
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("📝 Step 3: Symptom Details", expanded=False):
#             show_step_indicator(3)
#             st.markdown("### Provide more details about each symptom")
#             progress_bar = st.progress(0)
#             total_symptoms = len(primary_symptoms)
            
#             for i, symptom in enumerate(primary_symptoms):
#                 with st.container():
#                     icon = SYMPTOM_DEFINITIONS.get(symptom, {}).get("icon", "ℹ️")
#                     st.markdown(f"<div class='symptom-card'><h4>{icon} {symptom.replace('_', ' ').title()}</h4></div>", unsafe_allow_html=True)
                    
#                     if symptom in SYMPTOM_DEFINITIONS:
#                         symptom_score = 0
#                         for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                             if question["type"] == "radio":
#                                 response = st.radio(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}",
#                                     horizontal=True
#                                 )
#                                 symptom_score += question["weights"][response]
#                             elif question["type"] == "selectbox":
#                                 response = st.selectbox(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}"
#                                 )
#                                 symptom_score += question["weights"][response]
#                             elif question["type"] == "checkbox":
#                                 response = st.multiselect(
#                                     question["question"],
#                                     options=question["options"],
#                                     key=f"{symptom}_{question['question']}"
#                                 )
#                                 for item in response:
#                                     symptom_score += question["weights"][item]
#                         symptom_details[symptom] = symptom_score
#                     else:
#                         severity = st.slider(
#                             f"Severity of {symptom.replace('_', ' ')}",
#                             min_value=0.1, 
#                             max_value=3.0, 
#                             value=1.0, 
#                             step=0.1, 
#                             key=symptom,
#                             help="1 = Mild, 3 = Severe"
#                         )
#                         symptom_details[symptom] = severity
                    
#                     progress_bar.progress((i + 1) / total_symptoms)
#                     if i < total_symptoms - 1:
#                         st.divider()
    
#     # Step 4: Analysis
#     show_step_indicator(4 if primary_symptoms else 3)
#     if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             st.stop()
        
#         with st.spinner("Analyzing symptoms..."):
#             # Add a slight delay for better UX
#             time.sleep(1)
            
#             # Prepare input features
#             input_features = {col: 0.0 for col in all_symptoms}
#             input_features["AGE_FEATURE"] = 3 if age < 3 else (2 if age < 12 else 1)
#             input_features["IMMUNOCOMPROMISED_FEATURE"] = 1 if "Immunocompromised" in medical_history else 0
            
#             for symptom, score in symptom_details.items():
#                 if symptom in input_features:
#                     input_features[symptom] = score
            
#             # Make prediction
#             input_df = pd.DataFrame([input_features])
#             prediction = model.predict(input_df)[0]
#             probabilities = model.predict_proba(input_df)[0]
#             prediction = label_encoder.inverse_transform([prediction])[0]

#             # red_flags = []
#             if age < 3:
#                 red_flags.append("⚠️ Infants under 3 months are at higher risk for complicating conditions.")
#             if "Asthma" in medical_history:
#                 red_flags.append("⚠️ Caution: Child has a history of asthma.")
#             if "Prematurity or Neonatal Complications" in medical_history:
#                 red_flags.append("⚠️ Caution: Child was born prematurely or had neonatal complications, may need extra observation.")
#             if "Allergies (Food, Environmental, Medication)" in medical_history:
#                 red_flags.append("⚠️ Caution: Child has allergies which may complicate symptoms.")
            
#             # Get red flags
#             red_flags = []
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])
                    
            
#             # Generate recommendations
#             recommendations = []
#             if "Meningitis" in prediction:
#                 recommendations.append("EMERGENCY: Seek immediate medical attention - This is a medical emergency requiring IV antibiotics.")
#             if "Immunocompromised" in medical_history:
#                 recommendations.append("Children with compromised immune systems should be evaluated earlier for infections.")
#             if "FEVER" in primary_symptoms and age < 3:
#                 recommendations.append("Infants under 3 months with fever should be evaluated by a doctor immediately.")
#             if "DEHYDRATION" in primary_symptoms:
#                 recommendations.append("Ensure adequate fluid intake and monitor for worsening signs of dehydration.")
#             if "RESPIRATORY_DISTRESS" in primary_symptoms:
#                 recommendations.append("Respiratory distress requires immediate medical evaluation.")
#             if "STRIDOR" in primary_symptoms:
#                 recommendations.append("Stridor may indicate airway obstruction - seek medical attention.")
#             if "NECK_STIFFNESS" in primary_symptoms:
#                 recommendations.append("Neck stiffness with fever requires urgent medical evaluation.")
            
#             # Display results
#             st.markdown("---")
#             st.markdown(f"""
#             <div class='diagnosis-highlight'>
#                 <h2 style='text-align:center;margin-bottom:0.5rem;'>Diagnostic Results</h2>
#                 <h3 style='text-align:center;color:#4a6fa5;margin-top:0;'>Most likely condition: {prediction}</h3>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Condition probabilities
#             st.markdown("### Condition Probabilities")
#             prob_df = pd.DataFrame({
#                 "Condition": label_encoder.classes_,
#                 "Probability": probabilities
# }).sort_values("Probability", ascending=False).head(3)
            
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"}),
#                 column_config={
#                     "Condition": "Possible Condition",
#                     "Probability": st.column_config.ProgressColumn(
#                         "Probability",
#                         help="How likely this condition is",
#                         format="%.2f%%",
#                         min_value=0,
#                         max_value=1,
#                     )
#                 },
#                 hide_index=True,
#                 use_container_width=True
#             )
            
#             # Red flags
#             if red_flags:
#                 st.markdown("### ⚠️ Red Flags")
#                 for flag in red_flags:
#                     st.markdown(f"""
#                     <div class='red-flag'>
#                         <p style='margin:0;'><strong>{flag}</strong></p>
#                     </div>
#                     """, unsafe_allow_html=True)
#             else:
#                 st.markdown("""
#                 <div class='card' style='background-color:#e8f5e9;'>
#                     <h4 style='color:#2e7d32;margin:0;'>No urgent red flags identified</h4>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # Recommendations
#             if recommendations:
#                 st.markdown("### Recommended Actions")
#                 for rec in recommendations:
#                     st.markdown(f"""
#                     <div class='recommendation'>
#                         <p style='margin:0;'>{rec}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
            
#             # Additional advice based on condition
#             st.markdown("### ℹ️ Additional Information")
#             if "Common Cold" in prediction:
#                 st.markdown("""
#                 <div class='info-card'>
#                     <p><strong>For common cold:</strong></p>
#                     <ul>
#                         <li>Ensure your child gets plenty of rest</li>
#                         <li>Use saline nasal drops to relieve congestion</li>
#                         <li>Offer warm fluids to soothe throat irritation</li>
#                         <li>Use a cool-mist humidifier in the room</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)
#             elif "Gastroenteritis" in prediction:
#                 st.markdown("""
#                 <div class='info-card'>
#                     <p><strong>For gastroenteritis:</strong></p>
#                     <ul>
#                         <li>Offer small, frequent amounts of oral rehydration solution</li>
#                         <li>Avoid sugary drinks and dairy products</li>
#                         <li>Gradually reintroduce bland foods (BRAT diet: bananas, rice, applesauce, toast)</li>
#                         <li>Watch for signs of dehydration</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)
#             elif "Asthma" in prediction:
#                 st.markdown("""
#                 <div class='info-card'>
#                     <p><strong>For asthma:</strong></p>
#                     <ul>
#                         <li>Use prescribed inhalers as directed</li>
#                         <li>Avoid known triggers (dust, pollen, smoke)</li>
#                         <li>Seek emergency care if breathing becomes difficult</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)
#             elif "Meningitis" in prediction:
#                 st.markdown("""
#                 <div class='info-card'>
#                     <p><strong>For suspected meningitis:</strong></p>
#                     <ul>
#                         <li>This is a medical emergency - seek immediate care</li>
#                         <li>Do not wait - go to the nearest emergency department</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # PDF Report
#             st.markdown("---")
#             st.markdown("### 📄 Download Report")
#             pdf = generate_pdf_report(
#                 patient_info={"age": age, "medical_history": medical_history},
#                 symptoms=symptom_details,
#                 prediction=prediction,
#                 probabilities_df=prob_df,
#                 red_flags=red_flags,
#                 recommendations=recommendations
#             )
            
#             pdf_output = pdf.output(dest='S').encode('latin-1')
#             b64 = base64.b64encode(pdf_output).decode()
#             href = f"""
#             <a href="data:application/octet-stream;base64,{b64}" download="pediatric_health_report.pdf" style='
#                 display: inline-block;
#                 background-color: #4a6fa5;
#                 color: white;
#                 padding: 12px 24px;
#                 text-align: center;
#                 text-decoration: none;
#                 font-size: 16px;
#                 margin: 4px 2px;
#                 cursor: pointer;
#                 border-radius: 8px;
#                 border: none;
#                 transition: all 0.3s ease;
#             ' onmouseover="this.style.backgroundColor='#166088'" onmouseout="this.style.backgroundColor='#4a6fa5'">📥 Download Full Medical Report</a>
#             """
#             st.markdown(href, unsafe_allow_html=True)
    
#     # Nearby doctors section
#     st.markdown("---")
#     show_nearby_doctors()
    
#     # Footer
#     st.markdown("""
#     <div class="footer">
#         <p>This tool is for informational purposes only and does not provide medical advice.</p>
#         <p>Always consult a qualified healthcare provider for diagnosis and treatment.</p>
#         <p style="font-size:0.8em;margin-top:1rem;">Version 1.1.0 | Last updated: {date}</p>
#     </div>
#     """.format(date=datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()




import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
import requests
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from fpdf import FPDF
import base64
from datetime import datetime
import time
import random


# Custom CSS for modern UI
def local_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4a6fa5;
            --secondary: #166088;
            --accent: #4fc1e9;
            --background: #f8f9fa;
            --card: #ffffff;
            --text: #2c3e50;
            --warning: #ff6b6b;
            --success: #48dbb4;
            --info: #5bc0de;
        }
        
        .main {
            background-color: var(--background);
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            color: white;
            text-align: center;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            background-color: var(--secondary);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* Primary button */
        .primary-button {
            background-color: var(--primary) !important;
            color: white !important;
        }
        
        /* Secondary button */
        .secondary-button {
            background-color: var(--secondary) !important;
            color: white !important;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: var(--accent);
        }
        
        /* Cards */
        .card {
            background-color: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: var(--primary);
            font-size: 1.1rem;
        }
        
        .streamlit-expanderContent {
            padding: 1rem 1.5rem;
        }
        
        /* Alert boxes */
        .stAlert {
            border-radius: 12px;
        }
        
        /* Custom components */
        .symptom-card {
            background-color: var(--card);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            border-left: 4px solid var(--accent);
        }
        
        .symptom-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .red-flag {
            background-color: rgba(255,107,107,0.1);
            border-left: 4px solid var(--warning);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 8px 8px 0;
            animation: pulse 2s infinite;
        }
        
        .recommendation {
            background-color: rgba(72,219,180,0.1);
            border-left: 4px solid var(--success);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 8px 8px 0;
        }
        
        .info-card {
            background-color: rgba(91,192,222,0.1);
            border-left: 4px solid var(--info);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 8px 8px 0;
        }
        
        .diagnosis-highlight {
            background: linear-gradient(135deg, rgba(74,111,165,0.1) 0%, rgba(22,96,136,0.1) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(74,111,165,0.2);
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255,107,107,0.4); }
            70% { box-shadow: 0 0 0 10px rgba(255,107,107,0); }
            100% { box-shadow: 0 0 0 0 rgba(255,107,107,0); }
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 20px;
            background-color: #f0f4f8;
            border-radius: 8px 8px 0 0 !important;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e1e8f0;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary) !important;
            color: white !important;
        }
        
        /* Input fields */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            border-radius: 8px !important;
            padding: 10px 12px !important;
        }
        
        /* Radio buttons */
        .stRadio [role="radiogroup"] {
            gap: 15px;
        }
        
        .stRadio [role="radio"] {
            padding: 8px 16px;
            border-radius: 8px;
            border: 1px solid #dfe3e8;
        }
        
        .stRadio [role="radio"][aria-checked="true"] {
            background-color: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        
        /* Sliders */
        .stSlider [role="slider"] {
            background-color: var(--primary) !important;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: #666;
            font-size: 0.9em;
            margin-top: 2rem;
            border-top: 1px solid #eee;
        }
        
        /* Tooltips */
        .stTooltip {
            border-radius: 8px !important;
            padding: 8px 12px !important;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header-container {
                padding: 1.5rem 1rem;
            }
            
            .stButton>button {
                padding: 0.5rem 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# PDF Report Generator
def generate_pdf_report(patient_info, symptoms, prediction, probabilities_df, red_flags, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Header with color
    pdf.set_fill_color(74, 111, 165)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "Pediatric Health Report", 0, 1, 'C', 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C', 1)
    pdf.ln(10)
    
    # Reset colors
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    
    # Patient Information
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Patient Information", 0, 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Age: {patient_info['age']} months", 0, 1)
    pdf.cell(0, 8, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", 0, 1)
    pdf.ln(5)
    
    # Symptoms
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Reported Symptoms", 0, 1)
    pdf.set_font("Arial", '', 12)
    for symptom, details in symptoms.items():
        pdf.cell(0, 8, f"- {symptom.replace('_', ' ').title()}: Severity score {details}", 0, 1)
    pdf.ln(5)
    
    # Diagnosis
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Diagnostic Assessment", 0, 1)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(74, 111, 165)  # Primary color
    pdf.cell(0, 8, f"Most Likely Condition: {prediction}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    
    # Probability table
    pdf.cell(0, 8, "Condition Probabilities:", 0, 1)
    col_width = pdf.w / 3
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(col_width, 8, "Condition", 1)
    pdf.cell(col_width, 8, "Probability", 1, 1)
    pdf.set_font("Arial", '', 12)
    
    for _, row in probabilities_df.iterrows():
        pdf.cell(col_width, 8, row['Condition'], 1)
        pdf.cell(col_width, 8, f"{row['Probability']:.2%}", 1, 1)
    pdf.ln(5)
    
    # Red Flags
    if red_flags:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(255, 107, 107)  # Warning color
        pdf.cell(0, 10, "Red Flags", 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 12)
        for flag in red_flags:
            pdf.cell(0, 8, f"- {flag}", 0, 1)
        pdf.ln(5)
    
    # Recommendations
    if recommendations:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(72, 219, 180)  # Success color
        pdf.cell(0, 10, "Recommendations", 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 12)
        for rec in recommendations:
            pdf.cell(0, 8, f"- {rec}", 0, 1)
        pdf.ln(5)
    
    # Disclaimer
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 8, "Disclaimer: This report is generated by an AI system and should not replace professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
    
    return pdf

# Load and preprocess the dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    symptom_cols = [col for col in df.columns if col != "CONDITION"]
    df[symptom_cols] = df[symptom_cols].fillna(0)
    return df

# Enhanced medical knowledge base with all symptoms from the dataset
SYMPTOM_DEFINITIONS = {
    "FEVER": {
        "follow_up": [
            {"question": "Temperature", "type": "radio",
             "options": ["<100.4°F", "100.4-102.2°F", "102.2-104°F", ">104°F"],
             "weights": {"<100.4°F": 1, "100.4-102.2°F": 2, "102.2-104°F": 3, ">104°F": 4}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
             "weights": {"<24 hours": 1, "1-3 days": 2, "3-7 days": 3, ">7 days": 4}}
        ],
        "red_flags": ["Fever >100.4°F in infants <3 months", "Fever >104°F"],
        "icon": "🌡️"
    },
    "COUGH": {
        "follow_up": [
            {"question": "Type", "type": "selectbox",
             "options": ["Dry", "Productive", "Barking", "Whooping"],
             "weights": {"Dry": 1, "Productive": 2, "Barking": 3, "Whooping": 4}},
            {"question": "Timing", "type": "radio",
             "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
             "weights": {"Daytime": 1, "Nighttime": 2, "With feeding": 2, "After exercise": 2, "All day": 3}}
        ],
        "red_flags": ["Whooping sound on inspiration", "Cough causing vomiting"],
        "icon": "🤧"
    },
    "RUNNY_NOSE": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "red_flags": ["Nasal discharge with foul odor"],
        "icon": "👃"
    },
    "SNEEZING": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["Occasional", "Frequent", "Constant"],
             "weights": {"Occasional": 1, "Frequent": 2, "Constant": 3}}
        ],
        "icon": "🤧"
    },
    "DIARRHEA": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
             "weights": {"2-4 loose stools/day": 1, "5-8 loose stools/day": 2, ">8 loose stools/day": 3, "Watery": 3}},
            {"question": "Appearance", "type": "selectbox",
             "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
             "weights": {"Loose": 1, "Mucoid": 2, "Bloody": 3, "Rice-water": 3}}
        ],
        "red_flags": ["Blood in stool", "Signs of dehydration"],
        "icon": "💩"
    },
    "DEHYDRATION": {
        "follow_up": [
            {"question": "Signs", "type": "checkbox",
             "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
             "weights": {"Dry mouth": 1, "No tears": 2, "Sunken eyes": 3, "Decreased urine output": 3, "Lethargy": 4}}
        ],
        "red_flags": ["Severe dehydration signs"],
        "icon": "💧"
    },
    "ABDOMINAL_PAIN": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe", "Doubled over"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3, "Doubled over": 4}},
            {"question": "Location", "type": "selectbox",
             "options": ["Generalized", "Upper abdomen", "Lower abdomen", "Right side", "Left side"],
             "weights": {"Generalized": 1, "Upper abdomen": 2, "Lower abdomen": 2, "Right side": 3, "Left side": 3}}
        ],
        "red_flags": ["Severe localized pain", "Pain lasting >6 hours"],
        "icon": "🤢"
    },
    "RASH": {
        "follow_up": [
            {"question": "Appearance", "type": "selectbox",
             "options": ["Macular", "Papular", "Vesicular", "Petechial/Purpuric"],
             "weights": {"Macular": 1, "Papular": 2, "Vesicular": 3, "Petechial/Purpuric": 4}},
            {"question": "Distribution", "type": "checkbox",
             "options": ["Face", "Trunk", "Extremities", "Palms/Soles", "Generalized"],
             "weights": {"Face": 1, "Trunk": 1, "Extremities": 1, "Palms/Soles": 2, "Generalized": 2}}
        ],
        "red_flags": ["Rash with fever", "Non-blanching rash"],
        "icon": "🔴"
    },
    "HEADACHE": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<1 hour", "1-4 hours", "4-24 hours", ">24 hours"],
             "weights": {"<1 hour": 1, "1-4 hours": 2, "4-24 hours": 3, ">24 hours": 4}}
        ],
        "red_flags": ["Severe headache with fever", "Headache with neck stiffness"],
        "icon": "🤕"
    },
    "CHEST_PAIN": {
        "follow_up": [
            {"question": "Type", "type": "selectbox",
             "options": ["Sharp", "Dull", "Burning", "Pressure"],
             "weights": {"Sharp": 1, "Dull": 2, "Burning": 2, "Pressure": 3}},
            {"question": "Associated Symptoms", "type": "checkbox",
             "options": ["Shortness of breath", "Palpitations", "Cough", "Fever"],
             "weights": {"Shortness of breath": 2, "Palpitations": 2, "Cough": 1, "Fever": 1}}
        ],
        "red_flags": ["Chest pain with shortness of breath", "Chest pain with palpitations"],
        "icon": "💔"
    },
    "ITCHING": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Location", "type": "checkbox",
             "options": ["Face", "Trunk", "Extremities", "Generalized"],
             "weights": {"Face": 1, "Trunk": 1, "Extremities": 1, "Generalized": 2}}
        ],
        "icon": "🦠"
    },
    "MUSCLE_ACHES": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", ">3 days"],
             "weights": {"<24 hours": 1, "1-3 days": 2, ">3 days": 3}}
        ],
        "icon": "💪"
    },
    "NAUSEA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Associated Symptoms", "type": "checkbox",
             "options": ["Vomiting", "Dizziness", "Headache", "Fever"],
             "weights": {"Vomiting": 2, "Dizziness": 1, "Headache": 1, "Fever": 1}}
        ],
        "icon": "🤢"
    },
    "NECK_STIFFNESS": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Associated Symptoms", "type": "checkbox",
             "options": ["Fever", "Headache", "Photophobia"],
             "weights": {"Fever": 3, "Headache": 2, "Photophobia": 2}}
        ],
        "red_flags": ["Neck stiffness with fever"],
        "icon": "🦴"
    },
    "PHOTOPHOBIA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "red_flags": ["Photophobia with headache and fever"],
        "icon": "👁️"
    },
    "POLYDIPSIA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "icon": "🚰"
    },
    "POLYURIA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "icon": "🚽"
    },
    "RESPIRATORY_DISTRESS": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Signs", "type": "checkbox",
             "options": ["Nasal flaring", "Retractions", "Grunting", "Cyanosis"],
             "weights": {"Nasal flaring": 2, "Retractions": 3, "Grunting": 3, "Cyanosis": 4}}
        ],
        "red_flags": ["Respiratory distress with cyanosis"],
        "icon": "😮‍💨"
    },
    "SORE_THROAT": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", ">3 days"],
             "weights": {"<24 hours": 1, "1-3 days": 2, ">3 days": 3}}
        ],
        "icon": "👄"
    },
    "STRIDOR": {
        "follow_up": [
            {"question": "Timing", "type": "radio",
             "options": ["Inspiratory", "Expiratory", "Both"],
             "weights": {"Inspiratory": 2, "Expiratory": 3, "Both": 4}}
        ],
        "red_flags": ["Stridor at rest"],
        "icon": "🎵"
    },
    "VOMITING": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["1-2 times", "3-5 times", ">5 times"],
             "weights": {"1-2 times": 1, "3-5 times": 2, ">5 times": 3}},
            {"question": "Content", "type": "selectbox",
             "options": ["Food", "Bile", "Blood"],
             "weights": {"Food": 1, "Bile": 2, "Blood": 3}}
        ],
        "red_flags": ["Projectile vomiting", "Vomiting blood"],
        "icon": "🤮"
    },
    "WEIGHT_LOSS": {
        "follow_up": [
            {"question": "Amount", "type": "radio",
             "options": ["<5% body weight", "5-10% body weight", ">10% body weight"],
             "weights": {"<5% body weight": 1, "5-10% body weight": 2, ">10% body weight": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<1 week", "1-4 weeks", ">4 weeks"],
             "weights": {"<1 week": 1, "1-4 weeks": 2, ">4 weeks": 3}}
        ],
        "red_flags": ["Rapid weight loss"],
        "icon": "⚖️"
    },
    "WHEEZING": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Timing", "type": "selectbox",
             "options": ["Occasional", "With activity", "At rest"],
             "weights": {"Occasional": 1, "With activity": 2, "At rest": 3}}
        ],
        "red_flags": ["Wheezing at rest"],
        "icon": "🎵"
    }
}

# Find nearby doctors using Overpass API
def find_nearby_doctors(lat, lon, radius=5000):
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
        node["amenity"="doctors"](around:{radius},{lat},{lon});
        node["amenity"="clinic"](around:{radius},{lat},{lon});
        node["healthcare"="doctor"](around:{radius},{lat},{lon});
        node["healthcare"="pediatrician"](around:{radius},{lat},{lon});
    );
    out center;
    """
    try:
        response = requests.get(overpass_url, params={'data': query})
        response.raise_for_status()
        data = response.json()
        doctors = []
        for element in data['elements']:
            name = element.get('tags', {}).get('name', 'Unknown')
            address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Address not available'))
            specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
            lat = element.get('lat', element.get('center', {}).get('lat'))
            lon = element.get('lon', element.get('center', {}).get('lon'))
            if lat and lon:
                doctors.append({'name': name, 'address': address, 'specialty': specialty, 'latitude': lat, 'longitude': lon})
        return pd.DataFrame(doctors)
    except Exception as e:
        st.error(f"Error fetching nearby doctors: {e}")
        return pd.DataFrame()

# Show nearby doctors interface
def show_nearby_doctors():
    with st.expander("🚑 Find Nearby Pediatricians & Clinics", expanded=False):
        st.markdown("### 🔍 Locate healthcare providers near you")
        
        # Initialize default location (New York)
        lat, lon = 40.7128, -74.0060
        
        # Address input section
        address = st.text_input("Enter your full address:", 
                              placeholder="e.g., 123 Main St, City, Country",
                              key="doctor_search_address")
        
        if address:
            geolocator = Nominatim(user_agent="pediatric-symptom-checker")
            try:
                location = geolocator.geocode(address)
                if location:
                    lat, lon = location.latitude, location.longitude
                    st.success(f"Found location: {lat:.4f}, {lon:.4f}")
                else:
                    st.warning("Address not found. Using default location.")
            except Exception as e:
                st.error(f"Geocoding error: {e}")
                st.warning("Using default location.")
        
        search_radius = st.slider("Search radius (meters)", 
                                500, 10000, 2000, 
                                help="Wider radius may show more options")
        
        if st.button("🔍 Search for Doctors", type="primary", use_container_width=True):
            with st.spinner("Searching nearby..."):
                doctors_df = find_nearby_doctors(lat, lon, search_radius)
                
                if not doctors_df.empty:
                    st.success(f"✅ Found {len(doctors_df)} healthcare providers nearby")
                    
                    # Create map
                    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="cartodbpositron")
                    folium.Marker(
                        [lat, lon], 
                        popup="Your Location", 
                        icon=folium.Icon(color="blue", icon="user", prefix="fa")
                    ).add_to(m)
                    
                    # Add doctors
                    for idx, row in doctors_df.iterrows():
                        is_pediatric = "pediatric" in str(row['specialty']).lower()
                        icon_color = "green" if is_pediatric else "red"
                        icon_type = "child" if is_pediatric else "user-md"
                        
                        folium.Marker(
                            [row['latitude'], row['longitude']],
                            popup=f"<b>{row['name']}</b><br><i>{row['specialty']}</i><br>{row['address']}",
                            icon=folium.Icon(color=icon_color, icon=icon_type, prefix="fa")
                        ).add_to(m)
                    
                    # Display map
                    folium_static(m, width=700, height=500)
                    
                    # Show table
                    st.markdown("### 🏥 Nearby Healthcare Providers")
                    st.dataframe(
                        doctors_df[['name', 'specialty', 'address']].rename(columns={
                            'name': 'Name',
                            'specialty': 'Specialty',
                            'address': 'Address'
                        }),
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.warning("No doctors found in this area. Try increasing the search radius.")

# Train the model
@st.cache_resource
def train_model(df):
    df["AGE_FEATURE"] = 0
    df["IMMUNOCOMPROMISED_FEATURE"] = 0
    label_encoder = LabelEncoder()
    df["CONDITION"] = label_encoder.fit_transform(df["CONDITION"])
    X = df.drop(columns=["CONDITION"])
    y = df["CONDITION"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))
    ])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return pipeline, label_encoder

# Step indicator component using Streamlit columns
def show_step_indicator(current_step):
    steps = [
        {"title": "Patient Info", "number": 1},
        {"title": "Select Symptoms", "number": 2},
        {"title": "Symptom Details", "number": 3},
        {"title": "Analysis", "number": 4}
    ]


    
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            # Determine the step state
            if step["number"] < current_step:
                step_state = "✅"  # Completed
                step_color = "#48dbb4"  # Success color
            elif step["number"] == current_step:
                step_state = "➡️"  # Current
                step_color = "#4a6fa5"  # Primary color
            else:
                step_state = str(step["number"])  # Not started
                step_color = "#e0e0e0"  # Gray
            
            # Create a container for each step
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <div style="
                        background-color: {step_color};
                        color: white;
                        width: 30px;
                        height: 30px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto;
                        font-weight: bold;
                    ">{step_state}</div>
                    <div style="font-weight: {'bold' if step['number'] == current_step else 'normal'};">
                        {step['title']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Define symptom conflicts
conflicting_symptoms = {
    "FEVER": ["HYPOTHERMIA"],
    "WHEEZING": ["STRIDOR"],
    "STRIDOR": ["WHEEZING"],
    "NECK_STIFFNESS": ["PHOTOPHOBIA"],
    "PHOTOPHOBIA": ["NECK_STIFFNESS"],
    "RESPIRATORY_DISTRESS": ["SORE_THROAT"],
    "VOMITING": ["NAUSEA"],
    # add more conflicts if needed
}

# Helper function to filter options based on conflicts
def filter_conflicting_options(all_options, current_selection, conflicts_dict):
    filtered = []
    for opt in all_options:
        conflicts = conflicts_dict.get(opt, [])
        # Exclude if any conflicting symptom is already selected
        if not any(conflict in current_selection for conflict in conflicts):
            filtered.append(opt)
    return filtered

# Main application
def main():
    st.set_page_config(
        page_title="Pediatric Symptom Checker", 
        page_icon="👶", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    local_css()
    
    # Header with gradient
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0;padding:0;">👶 Pediatric Symptom Checker</h1>
        <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">A smart tool to help parents assess their child's symptoms and get guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="card">
        <p>Welcome to the Pediatric Symptom Checker. This tool helps you evaluate your child's symptoms and provides 
        guidance on possible conditions. Please follow these steps:</p>
        <ol>
            <li>Provide basic information about your child</li>
            <li>Select all symptoms your child is experiencing</li>
            <li>Provide details about each symptom</li>
            <li>Get an assessment with recommendations</li>
        </ol>
        <p><strong>Remember:</strong> This tool doesn't replace professional medical advice.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data and model
    file_path = "pages/pediatric_dataset_30k.csv"
    df = load_data(file_path)
    model, label_encoder = train_model(df)
    all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
    # Step 1: Patient Information
    with st.expander("👤 Step 1: Patient Information", expanded=True):
        show_step_indicator(1)
        st.markdown("### Tell us about your child")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input(
                "Age (months)", 
                min_value=0, 
                max_value=216, 
                value=24, 
                step=1,
                help="Child's age in months (0-18 years)"
            )
            
            # Age category indicator
            if age < 12:
                st.info("👶 Infant (0-12 months)")
            elif age < 36:
                st.info("🧒 Toddler (1-3 years)")
            elif age < 60:
                st.info("👦 Preschooler (3-5 years)")
            else:
                st.info("👧 Child (5+ years)")
                
        with col2:
            medical_history = st.multiselect(
                "Medical History (select all that apply)",
                options=["Allergies (Food, Environmental, Medication)", "Asthma", 
                         "Immunocompromised Status", "Prematurity or Neonatal Complications"],
                default=[]
            )
             # Set red flags based on medical history and age
            red_flags = []
            if "Immunocompromised Status" in medical_history:
                red_flags.append("Caution: Child with immunocompromised status.")
            if (age < 12) and ("Asthma" in medical_history):
                red_flags.append("Caution: Children with asthma are more vulnerable.")
            if (age < 3) and ("Allergies (Food, Environmental, Medication)" in medical_history):
                red_flags.append("Caution: Allergies may be more dangerous in infants.")
            
            # if "Immunocompromised" in medical_history:
            #     st.warning("⚠️ Children with compromised immune systems may need special medical attention")
    
    # Step 2: Symptom Selection
    with st.expander("🤒 Step 2: Select Symptoms", expanded=False):
        show_step_indicator(2)
        st.markdown("### What symptoms is your child experiencing?")
        
        # Updated symptom categories with five tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌡️ General Symptoms", 
            "🤢 Digestive Symptoms", 
            "🔴 Skin Symptoms", 
            "💨 Respiratory Symptoms", 
            "🧠 Neurological Symptoms"
        ])
        
        with tab1:
            general_symptoms = ["FEVER", "COUGH", "RUNNY_NOSE", "SNEEZING", "CHEST_PAIN", "MUSCLE_ACHES"]
            selected_general = st.multiselect(
                "General symptoms:",
                options=general_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select general symptoms...",
                key="general_symptoms"
            )

        with tab2:
            digestive_symptoms = ["DIARRHEA", "DEHYDRATION", "ABDOMINAL_PAIN", "NAUSEA", "VOMITING", "POLYDIPSIA", "POLYURIA", "WEIGHT_LOSS"]
            selected_digestive = st.multiselect(
                "Digestive symptoms:",
                options=digestive_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select digestive symptoms...",
                key="digestive_symptoms"
            )

        with tab3:
            skin_symptoms = ["RASH", "ITCHING"]
            selected_skin = st.multiselect(
                "Skin symptoms:",
                options=skin_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select skin symptoms...",
                key="skin_symptoms"
            )

        with tab4:
            respiratory_symptoms = ["COUGH", "WHEEZING", "STRIDOR", "RESPIRATORY_DISTRESS"]
            selected_respiratory = st.multiselect(
                "Respiratory symptoms:",
                options=respiratory_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select respiratory symptoms...",
                key="respiratory_symptoms"
            )

        with tab5:
            neurological_symptoms = ["HEADACHE", "NECK_STIFFNESS", "PHOTOPHOBIA"]
            selected_neurological = st.multiselect(
                "Neurological symptoms:",
                options=neurological_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select neurological symptoms...",
                key="neurological_symptoms"
            )

        # Combine all selected symptoms
        primary_symptoms = (selected_general + selected_digestive + selected_skin + 
                            selected_respiratory + selected_neurological)

        if primary_symptoms:
            st.markdown(f"<div class='info-card'>Selected symptoms: {', '.join([s.replace('_', ' ').title() for s in primary_symptoms])}</div>", unsafe_allow_html=True)
    
    # Step 3: Symptom Details
    symptom_details = {}
    if primary_symptoms:
        with st.expander("📝 Step 3: Symptom Details", expanded=False):
            show_step_indicator(3)
            st.markdown("### Provide more details about each symptom")
            progress_bar = st.progress(0)
            total_symptoms = len(primary_symptoms)
            
            for i, symptom in enumerate(primary_symptoms):
                with st.container():
                    icon = SYMPTOM_DEFINITIONS.get(symptom, {}).get("icon", "ℹ️")
                    st.markdown(f"<div class='symptom-card'><h4>{icon} {symptom.replace('_', ' ').title()}</h4></div>", unsafe_allow_html=True)
                    
                    if symptom in SYMPTOM_DEFINITIONS:
                        symptom_score = 0
                        for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
                            if question["type"] == "radio":
                                response = st.radio(
                                    question["question"],
                                    options=question["options"],
                                    key=f"{symptom}_{question['question']}",
                                    horizontal=True
                                )
                                symptom_score += question["weights"][response]
                            elif question["type"] == "selectbox":
                                response = st.selectbox(
                                    question["question"],
                                    options=question["options"],
                                    key=f"{symptom}_{question['question']}"
                                )
                                symptom_score += question["weights"][response]
                            elif question["type"] == "checkbox":
                                response = st.multiselect(
                                    question["question"],
                                    options=question["options"],
                                    key=f"{symptom}_{question['question']}"
                                )
                                for item in response:
                                    symptom_score += question["weights"][item]
                        symptom_details[symptom] = symptom_score
                    else:
                        severity = st.slider(
                            f"Severity of {symptom.replace('_', ' ')}",
                            min_value=0.1, 
                            max_value=3.0, 
                            value=1.0, 
                            step=0.1, 
                            key=symptom,
                            help="1 = Mild, 3 = Severe"
                        )
                        symptom_details[symptom] = severity
                    
                    progress_bar.progress((i + 1) / total_symptoms)
                    if i < total_symptoms - 1:
                        st.divider()
    
    # Step 4: Analysis
    show_step_indicator(4 if primary_symptoms else 3)
    if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
        if not primary_symptoms:
            st.warning("Please select at least one symptom")
            st.stop()
        
        with st.spinner("Analyzing symptoms..."):
            # Add a slight delay for better UX
            time.sleep(1)
            
            # Prepare input features
            input_features = {col: 0.0 for col in all_symptoms}
            input_features["AGE_FEATURE"] = 3 if age < 3 else (2 if age < 12 else 1)
            input_features["IMMUNOCOMPROMISED_FEATURE"] = 1 if "Immunocompromised" in medical_history else 0
            
            for symptom, score in symptom_details.items():
                if symptom in input_features:
                    input_features[symptom] = score
            
            # Make prediction
            input_df = pd.DataFrame([input_features])
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]
            prediction = label_encoder.inverse_transform([prediction])[0]

            # red_flags = []
            if age < 3:
                red_flags.append("⚠️ Infants under 3 months are at higher risk for complicating conditions.")
            if "Asthma" in medical_history:
                red_flags.append("⚠️ Caution: Child has a history of asthma.")
            if "Prematurity or Neonatal Complications" in medical_history:
                red_flags.append("⚠️ Caution: Child was born prematurely or had neonatal complications, may need extra observation.")
            if "Allergies (Food, Environmental, Medication)" in medical_history:
                red_flags.append("⚠️ Caution: Child has allergies which may complicate symptoms.")
            
            # Get red flags
            red_flags = []
            for symptom in primary_symptoms:
                if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
                    red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])
                    
            
            # Generate recommendations
            recommendations = []
            if "Meningitis" in prediction:
                recommendations.append("EMERGENCY: Seek immediate medical attention - This is a medical emergency requiring IV antibiotics.")
            if "Immunocompromised" in medical_history:
                recommendations.append("Children with compromised immune systems should be evaluated earlier for infections.")
            if "FEVER" in primary_symptoms and age < 3:
                recommendations.append("Infants under 3 months with fever should be evaluated by a doctor immediately.")
            if "DEHYDRATION" in primary_symptoms:
                recommendations.append("Ensure adequate fluid intake and monitor for worsening signs of dehydration.")
            if "RESPIRATORY_DISTRESS" in primary_symptoms:
                recommendations.append("Respiratory distress requires immediate medical evaluation.")
            if "STRIDOR" in primary_symptoms:
                recommendations.append("Stridor may indicate airway obstruction - seek medical attention.")
            if "NECK_STIFFNESS" in primary_symptoms:
                recommendations.append("Neck stiffness with fever requires urgent medical evaluation.")
            
            # Display results
            st.markdown("---")
            st.markdown(f"""
            <div class='diagnosis-highlight'>
                <h2 style='text-align:center;margin-bottom:0.5rem;'>Diagnostic Results</h2>
                <h3 style='text-align:center;color:#4a6fa5;margin-top:0;'>Most likely condition: {prediction}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Condition probabilities
            st.markdown("### Condition Probabilities")
            prob_df = pd.DataFrame({
                "Condition": label_encoder.classes_,
                "Probability": probabilities
}).sort_values("Probability", ascending=False).head(3)
            
            st.dataframe(
                prob_df.style.format({"Probability": "{:.2%}"}),
                column_config={
                    "Condition": "Possible Condition",
                    "Probability": st.column_config.ProgressColumn(
                        "Probability",
                        help="How likely this condition is",
                        format="%.2f%%",
                        min_value=0,
                        max_value=1,
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Red flags
            if red_flags:
                st.markdown("### ⚠️ Red Flags")
                for flag in red_flags:
                    st.markdown(f"""
                    <div class='red-flag'>
                        <p style='margin:0;'><strong>{flag}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='card' style='background-color:#e8f5e9;'>
                    <h4 style='color:#2e7d32;margin:0;'>No urgent red flags identified</h4>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendations
            if recommendations:
                st.markdown("### Recommended Actions")
                for rec in recommendations:
                    st.markdown(f"""
                    <div class='recommendation'>
                        <p style='margin:0;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Additional advice based on condition
            st.markdown("### ℹ️ Additional Information")
            if "Common Cold" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For common cold:</strong></p>
                    <ul>
                        <li>Ensure your child gets plenty of rest</li>
                        <li>Use saline nasal drops to relieve congestion</li>
                        <li>Offer warm fluids to soothe throat irritation</li>
                        <li>Use a cool-mist humidifier in the room</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif "Gastroenteritis" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For gastroenteritis:</strong></p>
                    <ul>
                        <li>Offer small, frequent amounts of oral rehydration solution</li>
                        <li>Avoid sugary drinks and dairy products</li>
                        <li>Gradually reintroduce bland foods (BRAT diet: bananas, rice, applesauce, toast)</li>
                        <li>Watch for signs of dehydration</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif "Asthma" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For asthma:</strong></p>
                    <ul>
                        <li>Use prescribed inhalers as directed</li>
                        <li>Avoid known triggers (dust, pollen, smoke)</li>
                        <li>Seek emergency care if breathing becomes difficult</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif "Meningitis" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For suspected meningitis:</strong></p>
                    <ul>
                        <li>This is a medical emergency - seek immediate care</li>
                        <li>Do not wait - go to the nearest emergency department</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # PDF Report
            st.markdown("---")
            st.markdown("### 📄 Download Report")
            pdf = generate_pdf_report(
                patient_info={"age": age, "medical_history": medical_history},
                symptoms=symptom_details,
                prediction=prediction,
                probabilities_df=prob_df,
                red_flags=red_flags,
                recommendations=recommendations
            )
            
            pdf_output = pdf.output(dest='S').encode('latin-1')
            b64 = base64.b64encode(pdf_output).decode()
            href = f"""
            <a href="data:application/octet-stream;base64,{b64}" download="pediatric_health_report.pdf" style='
                display: inline-block;
                background-color: #4a6fa5;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                border: none;
                transition: all 0.3s ease;
            ' onmouseover="this.style.backgroundColor='#166088'" onmouseout="this.style.backgroundColor='#4a6fa5'">📥 Download Full Medical Report</a>
            """
            st.markdown(href, unsafe_allow_html=True)
    
    # Nearby doctors section
    st.markdown("---")
    show_nearby_doctors()


    st.markdown("---")
    st.markdown("### 👪 Connect with Other Parents")
    st.markdown("Share your experiences and ask questions in our community forum.")
    if st.button("Open Parents Forum", type="secondary", use_container_width=True):
        st.switch_page("pages/chat.py") # This is the key line to switch pages


    st.markdown("---")
    st.markdown("### Growth Chart")
    st.markdown("Uderstand the growth of your child")
    if st.button("Open Growth Chart", type="secondary", use_container_width=True):
        st.switch_page("pages/growth.py") # This is the key line to switch pages
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>This tool is for informational purposes only and does not provide medical advice.</p>
        <p>Always consult a qualified healthcare provider for diagnosis and treatment.</p>
        <p style="font-size:0.8em;margin-top:1rem;">Version 1.1.0 | Last updated: {date}</p>
    </div>
    """.format(date=datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()