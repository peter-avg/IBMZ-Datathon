"""Main entry point for the AI-assisted Clinical Forms Streamlit application."""

import streamlit as st
import sys
import os

# Add the frontend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.state import initialize_session_state
from utils.config import config


def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="AI-assisted Clinical Forms",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main page content
    st.title("🏥 AI-assisted Clinical Forms")
    st.markdown("---")
    
    # Welcome message
    st.markdown("""
    ## Welcome to the AI-assisted Clinical Forms System
    
    This application helps doctors efficiently manage patient appointments by:
    
    - **Live Transcription**: Real-time audio capture and transcription during patient consultations
    - **AI-powered Extraction**: Automatic extraction of symptoms and medications from conversation
    - **Structured Forms**: Organized clinical forms with symptoms, medications, and notes
    - **Patient Management**: Complete patient database with form history
    
    ### Getting Started
    
    1. **Navigate to the Dashboard** using the sidebar to view all patients
    2. **Create a new patient** or select an existing one
    3. **Start a new form** for the patient
    4. **Begin a live session** to record and transcribe the consultation
    5. **Review and finalize** the form with AI-extracted information
    
    ### Features
    
    - 🎙️ **Live Audio Recording**: Browser-based audio capture using WebRTC
    - 🤖 **AI Entity Extraction**: Automatic detection of symptoms and medications
    - 📋 **Dynamic Forms**: Real-time form updates during consultation
    - 👥 **Patient Management**: Complete patient database and history
    - 📊 **Form Archive**: Historical form access and management
    
    ---
    """)
    
    # Configuration info
    with st.expander("🔧 Configuration", expanded=False):
        st.write("**Current Configuration:**")
        st.write(f"- Backend API URL: `{config.BACKEND_API_URL}`")
        st.write(f"- Default Doctor: `{config.DEFAULT_DOCTOR_NAME}`")
        st.write(f"- AI Autofill: `{'Enabled' if config.AI_AUTOFILL_ENABLED else 'Disabled'}`")
        st.write(f"- Mock API: `{'Enabled' if config.MOCK_API else 'Disabled'}`")
        
        if config.DEBUG:
            st.write("**Debug Mode:** Enabled")
    
    # Quick actions
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Go to Dashboard", type="primary", use_container_width=True):
            st.switch_page("pages/1_📋_Main_Dashboard.py")
    
    with col2:
        if st.button("👤 View Patients", use_container_width=True):
            st.switch_page("pages/1_📋_Main_Dashboard.py")
    
    with col3:
        if st.button("📝 New Form", use_container_width=True):
            st.switch_page("pages/3_📝_New_Form.py")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        AI-assisted Clinical Forms System | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
