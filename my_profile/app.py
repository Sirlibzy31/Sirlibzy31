import streamlit as st
import requests
import plotly.express as px
from streamlit_option_menu import option_menu
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

# Version Tracking
VERSION = "1.1.0"

def check_for_updates():
    """
    Check for potential updates
    """
    try:
        # Simulated update check
        latest_version = "1.1.0"  # This could come from an external source
        
        if latest_version > VERSION:
            st.sidebar.warning(f"""
            🔄 Update Available! 
            Current Version: {VERSION}
            Latest Version: {latest_version}
            
            Please contact the developer or 
            check the GitHub repository for updates.
            """)
        else:
            st.sidebar.success(f"✅ You're running the latest version {VERSION}")
    except Exception as e:
        st.sidebar.error(f"Version check failed: {e}")

def log_deployment():
    """
    Log deployment details
    """
    try:
        deployment_log_path = 'deployment_log.txt'
        with open(deployment_log_path, 'a') as log_file:
            log_entry = f"Deployed at: {datetime.now()} | Version: {VERSION}\n"
            log_file.write(log_entry)
    except Exception as e:
        st.error(f"Logging failed: {e}")

def send_email(name, email, message):
    """
    Send email from contact form
    """
    try:
        sender_email = st.secrets['SENDER_EMAIL']
        sender_password = st.secrets['SENDER_PASSWORD']
        recipient_email = st.secrets['RECIPIENT_EMAIL']

        if not all([name, email, message]):
            st.error("Please fill out all fields.")
            return False

        if '@' not in email or '.' not in email:
            st.error("Invalid email address.")
            return False

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Portfolio Contact: Message from {name}"

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True
    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False

def main():
    # Page Configuration
    st.set_page_config(
        page_title=f"Liberty Mutahwa | Portfolio (v{VERSION})",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Log Deployment
    log_deployment()

    # Custom CSS for Responsiveness and Styling
    st.markdown("""
    <style>
    /* Blue Header Modification */
    .stApp > header {
        background-color: #3498db !important;
        color: white !important;
    }
    
    /* Existing Styles */
    /* Responsive Base Styles */
    @media (max-width: 768px) {
        .main {
            padding: 10px !important;
        }
        .stColumn {
            width: 100% !important;
        }
        .skill-card {
            height: auto !important;
            margin-bottom: 10px;
        }
        .hero-section {
            padding: 15px !important;
        }
    }

    .main {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }
    .skill-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    .skill-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.2);
    }
    .hero-section {
        background: linear-gradient(135deg, #f6f8f9 0%, #e5ebee 100%);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        position: relative;
    }
    .profile-highlight {
        color: #2c3e50;
        font-weight: bold;
    }
    .circular-logo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        position: absolute;
        top: 10px;
        right: 10px;
        border: 3px solid #3498db;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .circular-logo:hover {
        transform: scale(1.1);
    }
    .version-badge {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background-color: #3498db;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

    # Version Badge
    st.markdown(f'<div class="version-badge">v{VERSION}</div>', unsafe_allow_html=True)

    # Check for Updates
    check_for_updates()

    # Navigation Menu
    with st.sidebar:
        # Add Version Information to Sidebar
        st.sidebar.info(f"Current Version: {VERSION}")
        
        selected = option_menu(
            menu_title="Portfolio Navigation",
            options=["Home", "Skills", "Projects", "Research Interests", "Contact"],
            icons=["house", "gear", "laptop", "book", "envelope"],
            menu_icon="code-slash",
            default_index=0,
        )

    # Home Page
    if selected == "Home":
        st.markdown("<div class='hero-section'>", unsafe_allow_html=True)
        
        # Circular Logo Placement
        st.markdown("""
        <img src="https://miro.medium.com/v2/resize:fit:1400/1*h-NxX0bCfPKqvWCLHS7oGQ.png" 
             class="circular-logo" 
             alt="Bioinformatics Logo">
        """, unsafe_allow_html=True)
        
        # Profile Header
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("# 🧬 Liberty Mutahwa")
            st.markdown("## Bioinformatics & Data Science Specialist")
            
            st.write("""
            🔬 A passionate bioinformatician at the intersection of biology and computational science, 
            dedicated to transforming complex biological data into actionable insights.

            ### Key Expertise
            - <span class='profile-highlight'>Genomic Analysis</span>
            - <span class='profile-highlight'>Machine Learning</span>
            - <span class='profile-highlight'>Drug Design</span>
            - <span class='profile-highlight'>Data Science</span>
            """, unsafe_allow_html=True)

            # Icons and Descriptions
            icon_cols = st.columns(4)
            icon_data = [
                {"icon": "🧬", "title": "Genomics", "description": "Data analysis and identification of biological patterns"},
                {"icon": "🤖", "title": "ML", "description": "Developing predictive models and extracting insights from complex datasets"},
                {"icon": "💊", "title": "Drug Design", "description": "Computational approaches to therapeutic innovation"},
                {"icon": "📊", "title": "Data Analysis", "description": "Extracting meaningful patterns from complex datasets"}
            ]
            for i, item in enumerate(icon_data):
                with icon_cols[i]:
                    st.markdown(f"<div style='text-align:center;'><span style='font-size:48px;'>{item['icon']}</span><br><strong>{item['title']}</strong><br>{item['description']}</div>", unsafe_allow_html=True)

        # Research Impact Section
        st.markdown("## 📊 Research Potential")
        
        research_metrics = {
            "Research Areas": 4,
            "Ongoing Projects": 2,
            "Technical Skills": 12
        }
        
        metric_cols = st.columns(3)
        for i, (metric, value) in enumerate(research_metrics.items()):
            with metric_cols[i]:
                st.metric(label=metric, value=value)

    # Skills Page
    elif selected == "Skills":
        st.header("🛠️ Technical Skills")
        skills_categories = {
            "Bioinformatics": {
                "Genomic Analysis": "Analyzing complex genetic data and identifying biological patterns",
                "Sequence Alignment": "Comparing DNA, RNA, and protein sequences to understand evolutionary relationships",
                "Phylogenetics": "Constructing evolutionary trees and studying genetic relationships",
                "RNA-Seq Analysis": "Examining gene expression levels and identifying differential expression"
            },
            "Programming": {
                "Python": "Versatile scripting for data analysis, machine learning, and automation",
                "R": "Statistical computing and graphics for scientific research",
                "Bash": "Shell scripting for system automation and data processing",
                "SQL": "Database querying and management for structured data"
            },
            "Data Science": {
                "Machine Learning": "Developing predictive models and extracting insights from complex datasets",
                "Statistical Analysis": "Applying advanced statistical methods to validate research hypotheses",
                "Data Visualization": "Creating informative and compelling visual representations of data",
                "Predictive Modeling": "Building algorithms to forecast trends and outcomes"
            },
            "Tools": {
                "Jupyter": "Interactive development environment for data science and research",
                "Streamlit": "Creating web applications for data science projects",
                "Git": "Version control and collaborative software development",
                "Docker": "Containerization for consistent and reproducible computing environments"
            }
        }
        
        for category, skills in skills_categories.items():
            st.subheader(category)
            cols = st.columns(len(skills))
            for i, (skill, description) in enumerate(skills.items()):
                with cols[i]:
                    st.markdown(f"<div class='skill-card'><strong>{skill}</strong><br>{description}</div>", unsafe_allow_html=True)

    # Projects Page
    elif selected == "Projects":
        st.header("💻 Research & Projects")
        projects = [
            {
                "name": "Genomic Variant Analysis",
                "description": "Developed machine learning models to predict genetic disease risks.",
                "technologies": ["Python", "Scikit-learn", "Pandas"],
                "impact": "Improved early disease detection algorithms"
            },
            {
                "name": "Drug Interaction Predictor",
                "description": "Created a computational framework for predicting potential drug interactions.",
                "technologies": ["R", "Bioconductor", "Machine Learning"],
                "impact": "Enhanced pharmaceutical research efficiency"
            }
        ]

        for project in projects:
            with st.expander(project["name"]):
                st.write(project["description"])
                st.write("Technologies:", ", ".join(project["technologies"]))
                st.write("Project Impact:", project["impact"])

    # Research Interests Page
    elif selected == "Research Interests":
        st.header("🔬 Research Focus")
        research_areas = [
            "Computational Genomics",
            "Machine Learning in Healthcare",
            "Precision Medicine",
            "Bioinformatics Algorithm Development"
        ]
        for area in research_areas:
            st.write(f"- {area}")

    # Contact Page
    elif selected == "Contact":
        st.header("📧 Get in Touch")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name", help="Enter your full name")
            email = st.text_input("Your Email", help="Enter a valid email address")
            message = st.text_area("Your Message", help="Write your message here")
            
            submitted = st.form_submit_button("Send Message")
            
            if submitted:
                if not name:
                    st.error("Please enter your name")
                elif not email or '@' not in email:
                    st.error("Please enter a valid email address")
                elif not message:
                    st.error("Please write a message")
                else:
                    with st.spinner('Sending message...'):
                        if send_email(name, email, message):
                            st.success("Message sent successfully! I'll get back to you soon.")
                            st.balloons()
                        else:
                            st.error("Failed to send the message. Please try again later.")

        # Contact Information
        st.write("### Contact Information")
        st.write("📞 WhatsApp: +263713144296")
        st.write("✉️ Email: mutahwalee@gmail.com")

        # External WhatsApp Contact with updated styling
        st.markdown(
            "<a href='https://wa.me/263713144296' target='_blank' style='display: block; width: 100%; text-align: center; background-color: #25D366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;'>Message on WhatsApp</a>", 
            unsafe_allow_html=True
        )

    # Deployment Timestamp in Sidebar
    st.sidebar.markdown(f"📅 Deployed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Global error handling sidebar
    st.sidebar.info("If you experience any issues, please refresh the page or contact support.")

if __name__ == "__main__":
    main()
