import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def run_form_submission_test():
    """
    Tests the complete form submission workflow including the
    doctor_patient relationship creation.
    """
    async with httpx.AsyncClient() as client:
        # --- Step 1: Create a new Doctor to get a valid doctor_id ---
        print("--- Step 1: Creating a new doctor ---")
        doctor_payload = {"full_name": "Dr. Marie Curie"}
        try:
            response = await client.post(f"{BASE_URL}/doctors/", json=doctor_payload)
            response.raise_for_status()
            new_doctor = response.json()
            doctor_id = new_doctor['doctor_id']
            print(f"✅ Doctor created with ID: {doctor_id}")
        except httpx.HTTPStatusError as e:
            print(f"❌ Failed to create doctor: {e.response.text}")
            return

        # --- Step 2: Create a new Patient to get a valid patient_id ---
        print("\n--- Step 2: Creating a new patient ---")
        patient_payload = {"full_name": "John Doe"}
        try:
            response = await client.post(f"{BASE_URL}/patients/", json=patient_payload)
            response.raise_for_status()
            new_patient = response.json()
            patient_id = new_patient['patient_id']
            print(f"✅ Patient created with ID: {patient_id}")
        except httpx.HTTPStatusError as e:
            print(f"❌ Failed to create patient: {e.response.text}")
            return

        # --- Step 3: Submit a Form with the new IDs ---
        print("\n--- Step 3: Submitting a new form ---")
        form_payload = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,  # doctor_id is now mandatory
            "symptoms": [
                {"name": "Headache", "intensity": 7, "duration": 2},
                {"name": "Fatigue"}
            ],
            "medications": [] # Testing the optional, empty medication list
        }
        
        try:
            response = await client.post(f"{BASE_URL}/forms/", json=form_payload)
            response.raise_for_status()
            form_response = response.json()
            print("✅ Form submitted successfully:")
            print(form_response)
        except httpx.HTTPStatusError as e:
            print(f"❌ Failed to submit form: {e.response.text}")
            return

        print("\n--- Test complete! ---")
        print("Check your 'doctor_patient', 'forms', 'symptoms', and 'form_symptom' tables in the database to verify.")

if __name__ == "__main__":
    asyncio.run(run_form_submission_test())