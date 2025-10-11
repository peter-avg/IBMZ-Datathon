"""Reusable patient card component."""

import streamlit as st
from typing import Optional
from datetime import date
from models.domain import Patient


def render_patient_card(patient: Patient, 
                       show_actions: bool = True,
                       card_key: Optional[str] = None) -> bool:
    """
    Render a patient card component.
    
    Args:
        patient: Patient data to display
        show_actions: Whether to show action buttons
        card_key: Optional unique key for the card
        
    Returns:
        True if "Open" button was clicked, False otherwise
    """
    if card_key is None:
        card_key = f"patient_card_{patient.id}"
    
    # Create card container
    with st.container():
        # Card header
        st.markdown(f"### {patient.name}")
        
        # Patient details
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Email
            if patient.email:
                st.write(f"📧 {patient.email}")
            
            # Date of birth
            if patient.date_of_birth:
                st.write(f"🎂 {patient.date_of_birth.strftime('%B %d, %Y')}")
            
            # Patient ID (smaller text)
            st.caption(f"ID: {patient.id}")
        
        with col2:
            # Avatar placeholder (using initials)
            initials = "".join([name[0].upper() for name in patient.name.split()[:2]])
            st.markdown(f"""
            <div style="
                width: 60px; 
                height: 60px; 
                border-radius: 50%; 
                background-color: #4CAF50; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                color: white; 
                font-size: 24px; 
                font-weight: bold;
                margin: 0 auto;
            ">
                {initials}
            </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        if show_actions:
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("👤 Open", key=f"{card_key}_open"):
                    return True
            
            with col2:
                if st.button("✏️ Edit", key=f"{card_key}_edit"):
                    st.session_state[f"{card_key}_edit_mode"] = True
                    st.rerun()
    
    return False


def render_patient_grid(patients: list[Patient], 
                       columns: int = 3,
                       grid_key: str = "patient_grid") -> Optional[Patient]:
    """
    Render a grid of patient cards.
    
    Args:
        patients: List of patients to display
        columns: Number of columns in the grid
        grid_key: Unique key for the grid
        
    Returns:
        Selected patient if "Open" was clicked, None otherwise
    """
    if not patients:
        st.info("No patients found. Create a new patient to get started.")
        return None
    
    # Create grid columns
    cols = st.columns(columns)
    
    selected_patient = None
    
    for i, patient in enumerate(patients):
        col_index = i % columns
        
        with cols[col_index]:
            if render_patient_card(patient, card_key=f"{grid_key}_{patient.id}"):
                selected_patient = patient
    
    return selected_patient


def render_patient_list(patients: list[Patient],
                       list_key: str = "patient_list") -> Optional[Patient]:
    """
    Render a list of patients with search functionality.
    
    Args:
        patients: List of patients to display
        list_key: Unique key for the list
        
    Returns:
        Selected patient if clicked, None otherwise
    """
    if not patients:
        st.info("No patients found.")
        return None
    
    selected_patient = None
    
    for patient in patients:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Patient name and details
                st.write(f"**{patient.name}**")
                if patient.email:
                    st.caption(f"📧 {patient.email}")
                if patient.date_of_birth:
                    st.caption(f"🎂 {patient.date_of_birth.strftime('%B %d, %Y')}")
            
            with col2:
                # Avatar
                initials = "".join([name[0].upper() for name in patient.name.split()[:2]])
                st.markdown(f"""
                <div style="
                    width: 40px; 
                    height: 40px; 
                    border-radius: 50%; 
                    background-color: #2196F3; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    color: white; 
                    font-size: 16px; 
                    font-weight: bold;
                ">
                    {initials}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("Open", key=f"{list_key}_{patient.id}_open"):
                    selected_patient = patient
            
            st.markdown("---")
    
    return selected_patient
