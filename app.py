from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FHIR_SERVER_URL = "https://hapi.fhir.org/baseR4/Patient"

def get_mock_patients():
    """Returns mock patient data for offline/fallback mode."""
    return [
        {
            "id": "mock-1",
            "name": "John Doe (Mock)",
            "gender": "male",
            "birthDate": "1980-01-01"
        },
        {
            "id": "mock-2",
            "name": "Jane Smith (Mock)",
            "gender": "female",
            "birthDate": "1990-05-15"
        },
        {
            "id": "mock-3",
            "name": "Alex Johnson (Mock)",
            "gender": "other",
            "birthDate": "2000-12-20"
        }
    ]

def parse_patient(resource):
    """Extracts relevant fields from a FHIR Patient resource."""
    try:
        pid = resource.get('id', 'N/A')
        
        # Handle name (array of HumanName)
        name_list = resource.get('name', [])
        full_name = "Unknown"
        if name_list:
            # Try to construct text or use family/given
            primary_name = name_list[0]
            if 'text' in primary_name:
                full_name = primary_name['text']
            else:
                family = primary_name.get('family', '')
                given = " ".join(primary_name.get('given', []))
                full_name = f"{given} {family}".strip()
        
        gender = resource.get('gender', 'Unknown')
        birth_date = resource.get('birthDate', 'N/A')
        
        return {
            "id": pid,
            "name": full_name,
            "gender": gender,
            "birthDate": birth_date
        }
    except Exception as e:
        logger.error(f"Error parsing patient resource: {e}")
        return {
            "id": resource.get('id', 'Error'),
            "name": "Parse Error",
            "gender": "N/A",
            "birthDate": "N/A"
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    patients = []
    error_message = None
    is_offline = False
    search_query = ""

    if request.method == 'POST':
        search_query = request.form.get('patient_name', '').strip()
        if search_query:
            try:
                # Prepare FHIR query parameters
                params = {'name': search_query}
                response = requests.get(FHIR_SERVER_URL, params=params, timeout=5)
                response.raise_for_status()
                
                fhir_data = response.json()
                
                if 'entry' in fhir_data:
                    for entry in fhir_data['entry']:
                        if 'resource' in entry:
                            patients.append(parse_patient(entry['resource']))
                else:
                    # No results found, but successful query
                    pass
                    
            except (requests.RequestException, ValueError) as e:
                logger.error(f"FHIR API Error: {e}")
                error_message = "Unable to connect to FHIR server. Showing mock data."
                is_offline = True
                patients = get_mock_patients()
                # Filter mock data if needed to match query loosely
                patients = [p for p in patients if search_query.lower() in p['name'].lower()]

    return render_template('index.html', patients=patients, error_message=error_message, is_offline=is_offline, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
