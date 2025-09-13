pip install fastapi uvicorn pandas matplotlib
backend_code = r'''
from fastapi import FastAPI
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # use non-interactive backend for server
import matplotlib.pyplot as plt
import io, base64

app = FastAPI()

# Load dataset
try:
    df = pd.read_csv("argo_sample.csv")
except Exception as e:
    df = pd.DataFrame()  # empty until file is present

@app.get("/")
def home():
    return {"message": "Welcome to floatChat Backend - AI Specialist for ARGO Data"}

@app.get("/ask")
def ask(query: str):
    q = query.lower()
    if "temperature" in q:
        # return quick dataset-driven summary if available
        if not df.empty:
            top = df.sort_values("Depth").iloc[0]["Temperature"]
            bottom = df.sort_values("Depth").iloc[-1]["Temperature"]
            return {"answer": f"As an AI Specialist: surface temp ≈ {top}°C, deep temp ≈ {bottom}°C. Temperature generally decreases with depth."}
        return {"answer": "As an AI Specialist: temperature generally decreases with depth in ARGO profiles."}
    elif "salinity" in q:
        return {"answer": "As an AI Specialist: salinity often changes slightly with depth (check plotted profile)."}
    elif "depth" in q:
        return {"answer": "As an AI Specialist: ARGO floats commonly profile from surface to ~1000 m (some go deeper)."}
    else:
        return {"answer": "I can answer about temperature, salinity, depth — try queries like 'show temperature' or 'explain salinity'."}

@app.get("/plot")
def plot(parameter: str = "Temperature"):
    if df.empty:
        return {"error": "Dataset not loaded. Place argo_sample.csv in the working directory."}
    if parameter not in df.columns:
        return {"error": f"Parameter '{parameter}' not found. Available columns: {list(df.columns)}"}
   
    plt.figure(figsize=(6,4))
    plt.plot(df[parameter], df["Depth"], marker="o")
    plt.gca().invert_yaxis()
    plt.title(f"{parameter} vs Depth")
    plt.xlabel(parameter)
    plt.ylabel("Depth (m)")
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return {"plot": img_base64}
'''
with open("floatchat_backend.py", "w", encoding="utf-8") as f:
    f.write(backend_code)
print("Wrote floatchat_backend.py")
import subprocess, sys, time, requests
def server_is_up(url="http://127.0.0.1:8000/"):
    try:
        r = requests.get(url, timeout=1.0)
        return r.status_code == 200
    except Exception:
        return False

if server_is_up():
    print("Server already running at http://127.0.0.1:8000/")
else:
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "floatchat_backend:app", "--reload", "--port", "8000"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1.5)
    if server_is_up():
        print("Server started at http://127.0.0.1:8000/  (PID {})".format(proc.pid))
        globals()["_floatchat_uvicorn_proc"] = proc
    else:
        print("Failed to start server. Check the cell output for errors.")
        try:
            out, err = proc.communicate(timeout=1)
            print(err.decode("utf-8", errors="ignore"))
        except Exception:
            pass
import requests
from IPython.display import HTML, display
base = "http://127.0.0.1:8000"
try:
    r = requests.get(base + "/")
    print("Home:", r.json())
except Exception as e:
    print("Cannot reach server:", e)
try:
    r = requests.get(base + "/ask", params={"query":"Show me temperature profile"})
    print("Ask:", r.json())
except Exception as e:
    print("Ask error:", e)
try:
    r = requests.get(base + "/plot", params={"parameter":"Temperature"})
    j = r.json()
    if "plot" in j:
        display(HTML(f"<h4>Temperature vs Depth (from /plot)</h4><img src='data:image/png;base64,{j['plot']}'/>"))
    else:
        print("Plot error:", j)
except Exception as e:
    print("Plot error:", e)
proc = globals().get("_floatchat_uvicorn_proc", None)
if proc is None:
    print("No background server handle found in globals(). If you started server in a terminal, stop it there (Ctrl+C).")
else:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    print("Server stopped.")
    globals().pop("_floatchat_uvicorn_proc", None)
