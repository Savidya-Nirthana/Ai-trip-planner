import streamlit as st
import datetime
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="🌍 Travel Planner",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🌍 Travel Planner")
    st.markdown("Describe your dream trip and get a personalised itinerary instantly.")
    st.divider()
    st.markdown("**💡 Example prompts**")
    st.markdown("- Plan a 5-day trip to Goa")
    st.markdown("- 7-day Japan itinerary for couples")
    st.markdown("- Budget trip to Bali for 10 days")
    st.divider()
    if st.session_state.get("messages") and st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🌍 AI Travel Planner")
st.caption("Tell me where you want to go and I'll craft your perfect itinerary.")
st.divider()

# ── Input form ────────────────────────────────────────────────────────────────
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Where do you want to travel?",
        placeholder="e.g. Plan a 5-day trip to Goa for 2 people",
    )
    submit = st.form_submit_button("✈️ Generate Itinerary")

# ── Handle submit ─────────────────────────────────────────────────────────────
if submit and user_input.strip():
    with st.spinner("Planning your trip..."):
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": user_input},
                timeout=60,
            )
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                st.session_state.messages.insert(0, {
                    "query": user_input,
                    "answer": answer,
                    "time": datetime.datetime.now(),
                })
            else:
                st.error(f"Server error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend at `localhost:8000`. Make sure the API server is running.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# ── Show results ──────────────────────────────────────────────────────────────
if st.session_state.messages:
    latest = st.session_state.messages[0]

    st.subheader(f"🗺️ {latest['query']}")
    st.caption(f"Generated on {latest['time'].strftime('%d %b %Y at %H:%M')}")
    st.markdown(latest["answer"])
    st.caption("⚠️ AI-generated content. Verify prices and travel requirements before booking.")

    if len(st.session_state.messages) > 1:
        st.divider()
        st.subheader("📋 Previous Plans")
        for item in st.session_state.messages[1:]:
            with st.expander(f"🗺️ {item['query']} — {item['time'].strftime('%d %b, %H:%M')}"):
                st.markdown(item["answer"])