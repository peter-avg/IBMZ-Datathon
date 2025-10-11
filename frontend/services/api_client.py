"""HTTP API client for AI-assisted Clinical Forms application."""

import uuid
import requests
from datetime import datetime, date
from typing import List, Optional, Dict, Any, Union
from models.domain import (
    Doctor, Patient, Form, Symptom, Medication,
    CreatePatientRequest, CreateFormRequest, UpdateFormRequest,
    CreateSymptomRequest, UpdateSymptomRequest,
    CreateMedicationRequest, UpdateMedicationRequest,
    FormStatus,
    # Backend models
    BackendDoctor, BackendDoctorCreate, BackendDoctorUpdate,
    BackendPatient, BackendPatientCreate, BackendPatientUpdate,
    BackendFormCreate, BackendSymptomCreate, BackendMedicationCreate,
    # Adapter functions
    doctor_to_backend, patient_to_backend, symptom_to_backend,
    medication_to_backend, backend_doctor_to_frontend,
    backend_patient_to_frontend, backend_symptom_to_frontend,
    backend_medication_to_frontend
)
from utils.config import config


class APIError(Exception):
    """Custom exception for API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class HTTPAPIClient:
    """HTTP API client for backend integration."""
    
    def __init__(self):
        """Initialize the HTTP client."""
        self.base_url = config.BACKEND_API_URL.rstrip('/')
        self.timeout = 30
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> requests.Response:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            # Handle HTTP errors
            if response.status_code >= 400:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        error_msg += f": {error_data['detail']}"
                except:
                    error_msg += f": {response.text}"
                
                raise APIError(error_msg, response.status_code)
            
            return response
            
        except requests.exceptions.RequestException as e:
            raise APIError(f"Network error: {str(e)}")
    
    def _generate_id(self) -> str:
        """Generate a unique ID for frontend use."""
        return str(uuid.uuid4())
    
    # Doctor operations
    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        """Get a doctor by ID."""
        try:
            response = self._make_request('GET', f'/doctors/{doctor_id}')
            backend_doctor = BackendDoctor(**response.json())
            return backend_doctor_to_frontend(backend_doctor)
        except APIError as e:
            if e.status_code == 404:
                return None
            raise
    
    def list_doctors(self) -> List[Doctor]:
        """List all doctors."""
        try:
            response = self._make_request('GET', '/doctors/')
            backend_doctors = [BackendDoctor(**doc) for doc in response.json()]
            return [backend_doctor_to_frontend(doc) for doc in backend_doctors]
        except APIError:
            # If backend fails, return default doctor for demo
            return [Doctor(id="D001", name="Dr. Demo")]
    
    def create_doctor(self, doctor: Doctor) -> Doctor:
        """Create a new doctor."""
        backend_request = doctor_to_backend(doctor)
        response = self._make_request('POST', '/doctors/', backend_request.dict())
        backend_doctor = BackendDoctor(**response.json())
        return backend_doctor_to_frontend(backend_doctor)
    
    def update_doctor(self, doctor_id: str, **fields) -> Optional[Doctor]:
        """Update a doctor."""
        update_data = {}
        if 'name' in fields:
            update_data['full_name'] = fields['name']
        if 'email' in fields:
            update_data['email'] = fields['email']
        if 'phone' in fields:
            update_data['phone'] = fields['phone']
        
        if not update_data:
            return None
        
        response = self._make_request('PATCH', f'/doctors/{doctor_id}', update_data)
        backend_doctor = BackendDoctor(**response.json())
        return backend_doctor_to_frontend(backend_doctor)
    
    def delete_doctor(self, doctor_id: str) -> bool:
        """Delete a doctor."""
        try:
            self._make_request('DELETE', f'/doctors/{doctor_id}')
            return True
        except APIError as e:
            if e.status_code == 404:
                return False
            raise
    
    # Patient operations
    def create_patient(self, request: CreatePatientRequest) -> Patient:
        """Create a new patient."""
        # Convert frontend request to backend format
        backend_request = BackendPatientCreate(
            full_name=request.name,
            dob=request.date_of_birth,
            sex_at_birth=request.sex_at_birth,
            phone=request.phone,
            email=request.email
        )
        
        response = self._make_request('POST', '/patients/', backend_request.dict())
        backend_patient = BackendPatient(**response.json())
        return backend_patient_to_frontend(backend_patient)
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Get a patient by ID."""
        try:
            response = self._make_request('GET', f'/patients/{patient_id}')
            backend_patient = BackendPatient(**response.json())
            return backend_patient_to_frontend(backend_patient)
        except APIError as e:
            if e.status_code == 404:
                return None
            raise
    
    def list_patients(self, search: Optional[str] = None) -> List[Patient]:
        """List all patients, optionally filtered by search term."""
        try:
            response = self._make_request('GET', '/patients/')
            backend_patients = [BackendPatient(**p) for p in response.json()]
            patients = [backend_patient_to_frontend(p) for p in backend_patients]
            
            # Apply search filter (client-side since backend doesn't support it)
            if search:
                search_lower = search.lower()
                patients = [
                    p for p in patients 
                    if search_lower in p.name.lower() or 
                       (p.email and search_lower in p.email.lower())
                ]
            
            return patients
        except APIError:
            # If backend fails, return empty list
            return []
    
    def update_patient(self, patient_id: str, **fields) -> Optional[Patient]:
        """Update a patient."""
        update_data = {}
        if 'name' in fields:
            update_data['full_name'] = fields['name']
        if 'email' in fields:
            update_data['email'] = fields['email']
        if 'date_of_birth' in fields:
            update_data['dob'] = fields['date_of_birth']
        if 'phone' in fields:
            update_data['phone'] = fields['phone']
        if 'sex_at_birth' in fields:
            update_data['sex_at_birth'] = fields['sex_at_birth']
        
        if not update_data:
            return None
        
        try:
            response = self._make_request('PATCH', f'/patients/{patient_id}', update_data)
            backend_patient = BackendPatient(**response.json())
            return backend_patient_to_frontend(backend_patient)
        except APIError as e:
            if e.status_code == 404:
                return None
            raise
    
    def delete_patient(self, patient_id: str) -> bool:
        """Delete a patient."""
        try:
            self._make_request('DELETE', f'/patients/{patient_id}')
            return True
        except APIError as e:
            if e.status_code == 404:
                return False
            raise
    
    # Form operations (adapted for backend's single-submission model)
    def create_form(self, request: CreateFormRequest) -> Form:
        """Create a new form (stored in session state only)."""
        # Since backend doesn't support incremental form creation,
        # we create a form object in memory for the session
        form = Form(
            id=self._generate_id(),
            patient_id=request.patient_id,
            doctor_id=request.doctor_id,
            created_at=datetime.now(),
            status=FormStatus.DRAFT
        )
        return form
    
    def get_form(self, form_id: str) -> Optional[Form]:
        """Get a form by ID (not supported by backend)."""
        # Backend doesn't support form retrieval
        return None
    
    def list_forms(self, patient_id: Optional[str] = None) -> List[Form]:
        """List forms (not supported by backend)."""
        # Backend doesn't support form listing
        return []
    
    def update_form(self, form_id: str, **fields) -> Optional[Form]:
        """Update a form (not supported by backend)."""
        # Backend doesn't support form updates
        return None
    
    def delete_form(self, form_id: str) -> bool:
        """Delete a form (not supported by backend)."""
        # Backend doesn't support form deletion
        return False
    
    def submit_form(
        self, 
        patient_id: str, 
        doctor_id: str, 
        symptoms: List[Symptom], 
        medications: List[Medication]
    ) -> str:
        """Submit a complete form to the backend."""
        # Convert frontend models to backend format
        backend_symptoms = [symptom_to_backend(s) for s in symptoms]
        backend_medications = [medication_to_backend(m) for m in medications]
        
        backend_request = BackendFormCreate(
            patient_id=patient_id,
            doctor_id=doctor_id,
            symptoms=backend_symptoms,
            medications=backend_medications
        )
        
        response = self._make_request('POST', '/forms/', backend_request.dict())
        # Backend returns a string identifier
        return response.text.strip('"')
    
    # Symptom operations (session state only)
    def create_symptom(self, request: CreateSymptomRequest) -> Symptom:
        """Create a new symptom (stored in session state)."""
        symptom = Symptom(
            id=self._generate_id(),
            form_id=request.form_id,
            name=request.name,
            duration=request.duration,
            intensity=request.intensity,
            recurrence=request.recurrence
        )
        return symptom
    
    def get_symptom(self, symptom_id: str) -> Optional[Symptom]:
        """Get a symptom by ID (not supported by backend)."""
        return None
    
    def list_symptoms(self, form_id: Optional[str] = None) -> List[Symptom]:
        """List symptoms (not supported by backend)."""
        return []
    
    def update_symptom(self, symptom_id: str, **fields) -> Optional[Symptom]:
        """Update a symptom (not supported by backend)."""
        return None
    
    def delete_symptom(self, symptom_id: str) -> bool:
        """Delete a symptom (not supported by backend)."""
        return False
    
    # Medication operations (session state only)
    def create_medication(self, request: CreateMedicationRequest) -> Medication:
        """Create a new medication (stored in session state)."""
        medication = Medication(
            id=self._generate_id(),
            form_id=request.form_id,
            name=request.name,
            strength=request.strength,
            frequency=request.frequency,
            duration=request.duration
        )
        return medication
    
    def get_medication(self, medication_id: str) -> Optional[Medication]:
        """Get a medication by ID (not supported by backend)."""
        return None
    
    def list_medications(self, form_id: Optional[str] = None) -> List[Medication]:
        """List medications (not supported by backend)."""
        return []
    
    def update_medication(self, medication_id: str, **fields) -> Optional[Medication]:
        """Update a medication (not supported by backend)."""
        return None
    
    def delete_medication(self, medication_id: str) -> bool:
        """Delete a medication (not supported by backend)."""
        return False
    
    # Utility methods
    def get_stats(self) -> Dict[str, int]:
        """Get storage statistics (not applicable for HTTP client)."""
        return {
            "doctors": 0,
            "patients": 0,
            "forms": 0,
            "symptoms": 0,
            "medications": 0
        }
    
    def clear_all_data(self):
        """Clear all data (not applicable for HTTP client)."""
        pass


class MockAPIClient:
    """Mock API client with in-memory storage for development and testing."""
    
    def __init__(self):
        """Initialize the mock client with empty storage."""
        self._doctors: Dict[str, Doctor] = {}
        self._patients: Dict[str, Patient] = {}
        self._forms: Dict[str, Form] = {}
        self._symptoms: Dict[str, Symptom] = {}
        self._medications: Dict[str, Medication] = {}
        
        # Initialize with default doctor
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize with default doctor for demo purposes."""
        default_doctor = Doctor(
            id="D001",
            name="Dr. Demo"
        )
        self._doctors[default_doctor.id] = default_doctor
    
    def _generate_id(self) -> str:
        """Generate a unique ID."""
        return str(uuid.uuid4())
    
    # Doctor operations
    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        """Get a doctor by ID."""
        return self._doctors.get(doctor_id)
    
    def list_doctors(self) -> List[Doctor]:
        """List all doctors."""
        return list(self._doctors.values())
    
    def create_doctor(self, doctor: Doctor) -> Doctor:
        """Create a new doctor."""
        doctor.id = self._generate_id()
        self._doctors[doctor.id] = doctor
        return doctor
    
    def update_doctor(self, doctor_id: str, **fields) -> Optional[Doctor]:
        """Update a doctor."""
        if doctor_id not in self._doctors:
            return None
        
        doctor = self._doctors[doctor_id]
        for field, value in fields.items():
            if hasattr(doctor, field):
                setattr(doctor, field, value)
        
        return doctor
    
    def delete_doctor(self, doctor_id: str) -> bool:
        """Delete a doctor."""
        if doctor_id in self._doctors:
            del self._doctors[doctor_id]
            return True
        return False
    
    # Patient operations
    def create_patient(self, request: CreatePatientRequest) -> Patient:
        """Create a new patient."""
        patient = Patient(
            id=self._generate_id(),
            name=request.name,
            email=request.email,
            date_of_birth=request.date_of_birth
        )
        self._patients[patient.id] = patient
        return patient
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Get a patient by ID."""
        return self._patients.get(patient_id)
    
    def list_patients(self, search: Optional[str] = None) -> List[Patient]:
        """List all patients, optionally filtered by search term."""
        patients = list(self._patients.values())
        
        if search:
            search_lower = search.lower()
            patients = [
                p for p in patients 
                if search_lower in p.name.lower() or 
                   (p.email and search_lower in p.email.lower())
            ]
        
        return patients
    
    def update_patient(self, patient_id: str, **fields) -> Optional[Patient]:
        """Update a patient."""
        if patient_id not in self._patients:
            return None
        
        patient = self._patients[patient_id]
        for field, value in fields.items():
            if hasattr(patient, field):
                setattr(patient, field, value)
        
        return patient
    
    def delete_patient(self, patient_id: str) -> bool:
        """Delete a patient."""
        if patient_id in self._patients:
            del self._patients[patient_id]
            return True
        return False
    
    # Form operations
    def create_form(self, request: CreateFormRequest) -> Form:
        """Create a new form."""
        form = Form(
            id=self._generate_id(),
            patient_id=request.patient_id,
            doctor_id=request.doctor_id,
            created_at=datetime.now(),
            status=FormStatus.DRAFT
        )
        self._forms[form.id] = form
        return form
    
    def get_form(self, form_id: str) -> Optional[Form]:
        """Get a form by ID."""
        return self._forms.get(form_id)
    
    def list_forms(self, patient_id: Optional[str] = None) -> List[Form]:
        """List forms, optionally filtered by patient ID."""
        forms = list(self._forms.values())
        
        if patient_id:
            forms = [f for f in forms if f.patient_id == patient_id]
        
        # Sort by created_at descending
        forms.sort(key=lambda f: f.created_at or datetime.min, reverse=True)
        return forms
    
    def update_form(self, form_id: str, **fields) -> Optional[Form]:
        """Update a form."""
        if form_id not in self._forms:
            return None
        
        form = self._forms[form_id]
        for field, value in fields.items():
            if hasattr(form, field):
                setattr(form, field, value)
        
        return form
    
    def delete_form(self, form_id: str) -> bool:
        """Delete a form and all associated symptoms/medications."""
        if form_id not in self._forms:
            return False
        
        # Delete associated symptoms and medications
        symptoms_to_delete = [s.id for s in self._symptoms.values() if s.form_id == form_id]
        medications_to_delete = [m.id for m in self._medications.values() if m.form_id == form_id]
        
        for symptom_id in symptoms_to_delete:
            del self._symptoms[symptom_id]
        
        for medication_id in medications_to_delete:
            del self._medications[medication_id]
        
        del self._forms[form_id]
        return True
    
    def submit_form(
        self, 
        patient_id: str, 
        doctor_id: str, 
        symptoms: List[Symptom], 
        medications: List[Medication]
    ) -> str:
        """Submit a complete form (mock implementation)."""
        return f"Form submitted for patient {patient_id}"
    
    # Symptom operations
    def create_symptom(self, request: CreateSymptomRequest) -> Symptom:
        """Create a new symptom."""
        symptom = Symptom(
            id=self._generate_id(),
            form_id=request.form_id,
            name=request.name,
            duration=request.duration,
            intensity=request.intensity,
            recurrence=request.recurrence
        )
        self._symptoms[symptom.id] = symptom
        return symptom
    
    def get_symptom(self, symptom_id: str) -> Optional[Symptom]:
        """Get a symptom by ID."""
        return self._symptoms.get(symptom_id)
    
    def list_symptoms(self, form_id: Optional[str] = None) -> List[Symptom]:
        """List symptoms, optionally filtered by form ID."""
        symptoms = list(self._symptoms.values())
        
        if form_id:
            symptoms = [s for s in symptoms if s.form_id == form_id]
        
        return symptoms
    
    def update_symptom(self, symptom_id: str, **fields) -> Optional[Symptom]:
        """Update a symptom."""
        if symptom_id not in self._symptoms:
            return None
        
        symptom = self._symptoms[symptom_id]
        for field, value in fields.items():
            if hasattr(symptom, field):
                setattr(symptom, field, value)
        
        return symptom
    
    def delete_symptom(self, symptom_id: str) -> bool:
        """Delete a symptom."""
        if symptom_id in self._symptoms:
            del self._symptoms[symptom_id]
            return True
        return False
    
    # Medication operations
    def create_medication(self, request: CreateMedicationRequest) -> Medication:
        """Create a new medication."""
        medication = Medication(
            id=self._generate_id(),
            form_id=request.form_id,
            name=request.name,
            strength=request.strength,
            frequency=request.frequency,
            duration=request.duration
        )
        self._medications[medication.id] = medication
        return medication
    
    def get_medication(self, medication_id: str) -> Optional[Medication]:
        """Get a medication by ID."""
        return self._medications.get(medication_id)
    
    def list_medications(self, form_id: Optional[str] = None) -> List[Medication]:
        """List medications, optionally filtered by form ID."""
        medications = list(self._medications.values())
        
        if form_id:
            medications = [m for m in medications if m.form_id == form_id]
        
        return medications
    
    def update_medication(self, medication_id: str, **fields) -> Optional[Medication]:
        """Update a medication."""
        if medication_id not in self._medications:
            return None
        
        medication = self._medications[medication_id]
        for field, value in fields.items():
            if hasattr(medication, field):
                setattr(medication, field, value)
        
        return medication
    
    def delete_medication(self, medication_id: str) -> bool:
        """Delete a medication."""
        if medication_id in self._medications:
            del self._medications[medication_id]
            return True
        return False
    
    # Utility methods
    def get_stats(self) -> Dict[str, int]:
        """Get storage statistics."""
        return {
            "doctors": len(self._doctors),
            "patients": len(self._patients),
            "forms": len(self._forms),
            "symptoms": len(self._symptoms),
            "medications": len(self._medications)
        }
    
    def clear_all_data(self):
        """Clear all data (useful for testing)."""
        self._doctors.clear()
        self._patients.clear()
        self._forms.clear()
        self._symptoms.clear()
        self._medications.clear()
        self._initialize_default_data()


# Global instance for the application
def get_api_client():
    """Get the appropriate API client based on configuration."""
    if config.MOCK_API:
        return MockAPIClient()
    else:
        return HTTPAPIClient()


# For backward compatibility
api_client = get_api_client()