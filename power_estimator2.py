import math
import streamlit as st

def estimate_watts(weight, speed, gradient, bike_type, distance):
    # Physical constants
    g = 9.81  # Accelerazione gravitazionale (m/s^2)
    rho = 1.225  # Densitá dell´aria (kg/m^3)
    
    # Conversions
    speed_ms = speed / 3.6  # Converti km/h in m/s
    angle = math.atan(gradient / 100)  # Converti % gradiente in angolo radiante
    
    # Total mass (ciclista + bici)
    bike_weight = 8 if bike_type == "road" else 12  # Peso bici in kg
    total_mass = weight + bike_weight  # Total mass (kg)
    
    # Aerodynamic and rolling resistance coefficients
    bike_data = {
        "road": {"CdA": 0.27, "Cr": 0.004},
        "MTB": {"CdA": 0.40, "Cr": 0.008},
        "TT": {"CdA": 0.23, "Cr": 0.003}
    }
    CdA = bike_data[bike_type]["CdA"]
    Cr = bike_data[bike_type]["Cr"]
    
    # Power due to air resistance
    P_air = 0.5 * CdA * rho * (speed_ms ** 3)
    
    # Power due to gravity
    P_gravity = total_mass * g * speed_ms * math.sin(angle)
    
    # Power due to rolling resistance
    P_rolling = total_mass * g * speed_ms * Cr
    
    # Total estimated power
    P_total = P_air + P_gravity + P_rolling
    
    # Estimated segment time (minutes)
    segment_time = (distance / speed) * 60  # Convert time from hours to minutes
    
    return round(P_total, 2), round(segment_time, 2)  # Return average power and time in minutes

def calculate_improvement(current_watts, current_time, desired_time, weight):
    # Watt necessari per tempo deisderato 
    improvement_ratio = current_time / desired_time
    new_watts = current_watts * improvement_ratio
    
    # Calcolo aumento di watt
    watt_increase = new_watts - current_watts
    
    # Calculate watts per kg ratio
    watts_per_kg = new_watts / weight
    
    return round(new_watts, 2), round(watts_per_kg, 2), round(watt_increase, 2)

# Streamlit UI
st.title("🚴 Bike Power Estimator 🏔️")
st.write("Estimate your cycling power ⚡ and how to improve 📈.")

# Info richieste ai ciclisti
weight = st.number_input("Enter your weight (kg):", min_value=30.0, max_value=150.0, value=70.0)
speed = st.number_input("Enter your average speed on the segment 🏎️ (km/h):", min_value=5.0, max_value=80.0, value=25.0)
gradient = st.number_input("Enter the average gradient of the segment 📈 (%):", min_value=-10.0, max_value=20.0, value=5.0)
bike_type = st.selectbox("Select bike type 🚲:", ["road", "MTB", "TT"])
distance = st.number_input("Enter the segment length (km):", min_value=0.1, max_value=50.0, value=5.0)

# Calcolo potenza e tempo 
power, time = estimate_watts(weight, speed, gradient, bike_type, distance)
st.success(f"Estimated average power ⚡: {power} watts.")
st.success(f"Estimated segment time ⏰: {time} minutes.")

# Miglioramento
if time > 1.1:  # Check intervallo valido
    time_improvement = st.slider("By how many minutes do you want to improve?", 0.1, max(time - 0.1, 0.1), 1.0)
    desired_time = time - time_improvement
    if desired_time > 0:
        new_watts, watts_per_kg, watt_increase = calculate_improvement(power, time, desired_time, weight)
        st.info(f"To improve your time by {time_improvement} minutes (target time 🕰️: {desired_time} min), "
                f"you need to increase your power by {watt_increase} watts.")
        st.info(f"This means generating a total of {new_watts} watts, which corresponds to {watts_per_kg} watts/kg.")
    else:
        st.warning("The desired time must be greater than zero. Adjust your improvement time.")
else:
    st.warning("⚠️ Your estimated time is too short to improve further. Try adjusting your speed or distance.")
    #  Pulsante
if st.button("Go!!! 🚴‍♂️🔥"):
    st.success("Go push on those pedals, or adjust values if you overestimated yourself!")

