import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time
 
st.set_page_config(page_title="Live Weather", page_icon="🌤️", layout="wide")
 
# Disable fade/transition so charts don't blink between reruns
st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)
 
st.title("🌤️ Live Denver Weather (Open-Meteo)")
st.caption("Current conditions from Open-Meteo. Responses are cached, and each reading is saved to a short history.")
 
# ---------------- Config ----------------
lat, lon = 39.7392, -104.9903  # Denver
wurl = (
    f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    "&current=temperature_2m,wind_speed_10m"
    "&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FDenver"
)
HEADERS = {"User-Agent": "msudenver-dataviz-class/1.0", "Accept": "application/json"}
MAX_POINTS = 100  # keep only the most recent readings
 
# Fallback so the page still works if the API is down
SAMPLE_DF = pd.DataFrame([{"time": pd.Timestamp.now(), "temperature": 55.0, "wind": 5.0}])
 
 
# ---------------- Fetch (cached) ----------------
@st.cache_data(ttl=600, show_spinner=False)  # cache for 10 minutes
def get_weather():
    """Return (df, error_message). Never raises."""
    try:
        r = requests.get(wurl, timeout=10, headers=HEADERS)
        if r.status_code == 429:
            retry_after = r.headers.get("Retry-After", "a bit")
            return None, f"429 Too Many Requests — try again after {retry_after}s"
        r.raise_for_status()
        j = r.json()["current"]
        df = pd.DataFrame([{
            "time": pd.to_datetime(j["time"]),
            "temperature": j["temperature_2m"],
            "wind": j["wind_speed_10m"],
        }])
        return df, None
    except (requests.RequestException, KeyError, ValueError) as e:
        return None, f"Network/API error: {e}"
 
 
# ---------------- Refresh controls ----------------
st.subheader("🔁 Auto Refresh Settings")
refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)
auto_refresh = st.toggle("Enable auto-refresh", value=False)
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")
 
if st.button("Clear history"):
    st.session_state.weather_history = []
 
 
# ---------------- Get data ----------------
df, err = get_weather()
if err:
    st.warning(f"{err}\nShowing sample data so the demo continues.")
    df = SAMPLE_DF.copy()
 
 
# ---------------- History in session state ----------------
if "weather_history" not in st.session_state:
    st.session_state.weather_history = []
 
row = df.iloc[0]
st.session_state.weather_history.append({
    "fetched_at": pd.Timestamp.now(tz="America/Denver").tz_localize(None),
    "api_time": row["time"],
    "temperature": float(row["temperature"]),
    "wind": float(row["wind"]),
})
st.session_state.weather_history = st.session_state.weather_history[-MAX_POINTS:]
hist = pd.DataFrame(st.session_state.weather_history)
 
 
# ---------------- Metrics ----------------
temp_now = hist["temperature"].iloc[-1]
wind_now = hist["wind"].iloc[-1]
temp_delta = temp_now - hist["temperature"].iloc[-2] if len(hist) > 1 else None
 
c1, c2, c3 = st.columns(3)
c1.metric("Temperature", f"{temp_now:.1f} °F",
          delta=f"{temp_delta:+.1f} °F" if temp_delta is not None else None)
c2.metric("Wind speed", f"{wind_now:.1f} mph")
c3.metric("Readings collected", len(hist))
 
 
# ---------------- Chart: temperature over time ----------------
fig = px.line(
    hist,
    x="fetched_at",
    y="temperature",
    markers=True,
    title="Denver Temperature Over Time",
)
fig.update_layout(xaxis_title="Time (Denver)", yaxis_title="Temperature (°F)")
st.plotly_chart(fig, use_container_width=True)
 
with st.expander("See history table"):
    st.dataframe(hist, use_container_width=True)
 
 
# ---------------- Auto refresh ----------------
if auto_refresh:
    time.sleep(refresh_sec)
    get_weather.clear()
    st.rerun()
 