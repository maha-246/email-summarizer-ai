import streamlit as st
import config
from backend import process_email

# 1. UI Page Setup
st.set_page_config(page_title="Email Summary Assistant", page_icon="📧")

st.sidebar.title("Config")
st.sidebar.caption(f"**Gemini:** {config.GEMINI_MODEL}")
st.sidebar.caption(f"**Groq:** {config.GROQ_MODEL}")
if config.MOCK_MODE:
    st.sidebar.warning("🛠️ MOCK MODE: ON")


st.title("📧 Email Summary Assistant")
st.write("Paste an email to get an AI summary.")
st.warning("⚠️ Do not paste sensitive data while using free API keys.")

# 2. User Input
with st.form("summary_form"):
    email_content = st.text_area("Paste email body here", height=250)
    submit_button = st.form_submit_button("Summarize Email")

# 3. Execution
if submit_button:
    if not config.GEMINI_API_KEY:
        st.error("Missing GEMINI_API_KEY. Please check your .env file.")
    else:
        with st.spinner("AI is thinking..."):
            # Notice how much cleaner this call is now!
            data, provider, error, warning = process_email(email_content)

        # Show Warnings/Errors
        if warning:
            st.warning(warning)
            
        if error:
            st.error(error)
        elif data:
            st.subheader(f"Summary ({provider})")
            
            # Provider info
            if provider == "Groq":
                st.info("Generated using Groq fallback.")
            else:
                st.info("Generated using Gemini.")

            # Display Fields
            st.write(f"**Summary:** {data.get('summary')}")
            st.write(f"**Priority:** {data.get('priority', 'medium').upper()}")
            
            st.write("**Important Details:**")
            for detail in data.get('important_details', []):
                st.write(f"- {detail}")
            
            st.write(f"**Action:** {data.get('required_action')}")
            st.write(f"**Deadline:** {data.get('deadline') or 'None'}")
            
            if data.get('sensitive_info_detected'):
                st.error("🚩 Sensitive information detected.")
            
            with st.expander("✨ View Suggested Reply"):
                st.write(data.get('suggested_reply'))
                
            st.success("Finished!")
