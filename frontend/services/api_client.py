"""Mock API client for AI-assisted Clinical Forms application."""

import uuid
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from models.domain import (
    Doctor, Patient, Form, Symptom, Medication,
    CreatePatientRequest, CreateFormRequest, UpdateFormRequest,
    CreateSymptomRequest, UpdateSymptomRequest,
    CreateMedicationRequest, UpdateMedicationRequest,
    FormStatus
)


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
api_client = MockAPIClient()

