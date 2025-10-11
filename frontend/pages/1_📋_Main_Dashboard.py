"""Main Dashboard page for AI-assisted Clinical Forms."""

import streamlit as st
from datetime import date
from typing import Optional
from models.domain import CreatePatientRequest
from services.api_client import api_client
from components.patient_card import render_patient_grid, render_patient_list
from utils.state import (
    initialize_session_state, 
    get_patient_search_query, 
    set_patient_search_query,
    toggle_create_patient_modal,
    is_create_patient_modal_open,
    set_current_patient
)
from utils.config import config


def render_sidebar():
    """Render the sidebar with patient list and search."""
    with st.sidebar:
        st.title("🏥 Clinical Forms")
        
        # Current doctor info
        current_doctor = st.session_state.get("current_doctor")
        if current_doctor:
            st.write(f"**Doctor:** {current_doctor.name}")
        
        st.markdown("---")
        
        # Patient search
        st.subheader("🔍 Search Patients")
        search_query = st.text_input(
            "Search by name or email",
            value=get_patient_search_query(),
            key="patient_search_input",
            placeholder="Enter patient name or email..."
        )
        set_patient_search_query(search_query)
        
        # Get filtered patients
        patients = api_client.list_patients(search=search_query if search_query else None)
        
        # Patient list in sidebar
        st.subheader("👥 Patients")
        if patients:
            selected_patient = render_patient_list(patients, "sidebar_patient_list")
            if selected_patient:
                set_current_patient(selected_patient)
                st.switch_page("pages/2_👤_Patient_Page.py")
        else:
            st.info("No patients found.")
        
        st.markdown("---")
        
        # Settings link (placeholder)
        if st.button("⚙️ Settings"):
            st.info("Settings page coming soon!")


def render_create_patient_modal():
    """Render the create patient modal."""
    if not is_create_patient_modal_open():
        return
    
    # Create modal using st.form
    with st.form("create_patient_form", clear_on_submit=True):
        st.subheader("➕ Create New Patient")
        
        # Form fields
        name = st.text_input("Full Name *", placeholder="Enter patient's full name")
        email = st.text_input("Email", placeholder="Enter patient's email address")
        date_of_birth = st.date_input("Date of Birth", value=None)
        
        # Form buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button("Create Patient", type="primary")
        
        with col2:
            cancel_button = st.form_submit_button("Cancel")
        
        # Handle form submission
        if submit_button:
            if not name.strip():
                st.error("Please enter a patient name.")
            else:
                try:
                    # Create patient request
                    request = CreatePatientRequest(
                        name=name.strip(),
                        email=email.strip() if email else None,
                        date_of_birth=date_of_birth if date_of_birth else None
                    )
                    
                    # Create patient via API
                    new_patient = api_client.create_patient(request)
                    
                    st.success(f"Patient '{new_patient.name}' created successfully!")
                    
                    # Close modal and refresh
                    toggle_create_patient_modal()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error creating patient: {str(e)}")
        
        if cancel_button:
            toggle_create_patient_modal()
            st.rerun()


def render_main_content():
    """Render the main content area with patient cards."""
    st.title("📋 Patient Dashboard")
    
    # Get search query and filter patients
    search_query = get_patient_search_query()
    patients = api_client.list_patients(search=search_query if search_query else None)
    
    # Display search results info
    if search_query:
        st.write(f"**Search results for:** '{search_query}' ({len(patients)} patients found)")
    else:
        st.write(f"**All patients:** {len(patients)} patients")
    
    st.markdown("---")
    
    # Patient grid
    if patients:
        selected_patient = render_patient_grid(patients, columns=3, grid_key="main_patient_grid")
        if selected_patient:
            set_current_patient(selected_patient)
            st.switch_page("pages/2_👤_Patient_Page.py")
    else:
        # Empty state
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3>No patients found</h3>
            <p>Create your first patient to get started with clinical forms.</p>
        </div>
        """, unsafe_allow_html=True)


def render_floating_action_button():
    """Render the floating action button for creating patients."""
    # Create a floating button using columns
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("➕ Add Patient", type="primary", use_container_width=True):
            toggle_create_patient_modal()
            st.rerun()


def main():
    """Main dashboard function."""
    # Initialize session state
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="Clinical Forms Dashboard",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Render sidebar
    render_sidebar()
    
    # Render main content
    render_main_content()
    
    # Render floating action button
    st.markdown("---")
    render_floating_action_button()
    
    # Render create patient modal
    render_create_patient_modal()


if __name__ == "__main__":
    main()
