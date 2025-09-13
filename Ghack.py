import pandas as pd
import matplotlib.pyplot as plt
try:
    df = pd.read_csv("argo_sample.csv")
    print("✅ ARGO dataset loaded successfully!")
    print(df.head())
except FileNotFoundError:
    print("⚠️ File 'argo_sample.csv' not found! Please place it in the same folder.")
def ai_specialist(query):
    """
    Simulates an AI Specialist who can answer questions
    about ARGO Ocean Data (temperature, salinity, oxygen).
    """
    query = query.lower()
    if "temperature" in query:
        return "As an AI Specialist, I observe that ARGO floats show decreasing temperature with depth."
    elif "salinity" in query:
        return "As an AI Specialist, I see salinity slightly increases with depth in most ARGO profiles."
    elif "oxygen" in query:
        return "As an AI Specialist, I note that oxygen concentration decreases as depth increases."
    elif "graph" in query:
        return "I can generate graphs for temperature, salinity, and oxygen against depth."
    else:
        return "I am your AI Specialist. Please ask me about temperature, salinity, oxygen, or graphs."
print("\n👩‍💻 User: Show me temperature data")
print("🤖 AI Specialist:", ai_specialist("Show me temperature data"))
print("\n👩‍💻 User: Explain salinity pattern")
print("🤖 AI Specialist:", ai_specialist("Explain salinity pattern"))
print("\n👩‍💻 User: Can you generate graph?")
print("🤖 AI Specialist:", ai_specialist("Can you generate graph?"))
def plot_profile(parameter):
    if parameter not in df.columns:
        print(f"⚠️ Column '{parameter}' not found in dataset.")
        return
    plt.figure(figsize=(6,4))
    plt.plot(df[parameter], df["Depth"], marker="o")
    plt.gca().invert_yaxis()  # Depth increases downward
    plt.title(f"{parameter} vs Depth (ARGO Float)")
    plt.xlabel(parameter)
    plt.ylabel("Depth (m)")
    plt.grid(True)
    plt.show()
plot_profile("Temperature")
