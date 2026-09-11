# Fieldwise Crop Recommendation

Fieldwise recommends a crop from the labeled profiles in `recomendation.csv` using normalized distance across seven soil and climate features. The repository includes a dependency-free Python web API, a browser interface, and an optional Random Forest training script.

---

## 📌 Project Objective

To develop a **smart crop recommendation system** that collects real-time environmental data via sensors and uses a trained **Machine Learning model** to suggest the best crop to grow.

---

## Components

- Arduino Uno + Sensors (Soil Moisture, pH, MQ135, LDR, TMP36, Rain Sensor)
- Python (Data Processing, Visualization, ML)
- Machine Learning (Random Forest Classifier)
- Pandas, scikit-learn, and joblib for optional model training

---

## 🔧 Hardware Setup

Sensors connected to Arduino Uno:
- A0 – Soil Moisture Sensor  
- A1 – pH Sensor  
- A2 – MQ135 (Air Quality)  
- A3 – LDR (Light Intensity)  
- A4 – Rain Sensor  
- A5 – TMP36 (Temperature Sensor)

📍 **Sensor data is sent to Python through Serial Communication.**

---

## 🧠 Machine Learning Workflow

1. **Data Collection** from CSV or real-time Arduino serial.
2. **Model Training** using Random Forest Classifier.
3. **Real-Time Prediction** using live Arduino data.
4. **Graph Comparison** with historical crop data using DTW.

---

## 🖥️ How to Run the Project

### Run the web app locally

Start the network-ready frontend and prediction API from this folder:

```bash
python server.py
```

Then open `http://localhost:8000` on the host computer. The server also prints a LAN URL such as `http://192.168.x.x:8000`; devices on the same Wi-Fi can use that address.

The server binds to `0.0.0.0` by default and reads `PORT` and `HOST` when provided. It exposes `GET /api/health`, `GET /api/profiles`, and `POST /api/predict`. The API validates all values and has no authentication, so place it behind an authenticated reverse proxy before exposing it publicly.

Use another port when needed:

```bash
python server.py --port 8080
```

### Run with Docker

```bash
docker build -t fieldwise .
docker run --rm -p 8000:8000 fieldwise
```

### Retrain the optional Random Forest model

Install the training dependencies and run:

   ```bash
   python -m pip install -r requirements.txt
   python Precision_Agriculture.py
   ```

---

## 📊 Graphical Analysis

- Real-time sensor readings are plotted.
- Spline interpolation smooths the graph.
- DTW compares new data with ideal crop profiles.
- Outputs similarity % and top matching crops.

---

## File Structure

```
📦 Project Root
├── recomendation.csv           # Labeled profiles used by the API
├── server.py                   # Web server and prediction API
├── code.html                   # Browser interface
├── Precision_Agriculture.py    # Optional Random Forest training script
├── Dockerfile                  # Production container for the API and UI
└── requirements.txt            # Training dependencies
```

---

## ✅ Results

The API returns the closest profile and a relative confidence score. Evaluate any retrained classifier on a held-out test set before using it for agronomic decisions.

---

## 🚀 Future Scope

- Mobile app with sensor integration  
- Smart irrigation automation  
- GPS-based location-aware suggestions  

---

## 📝 Credits

- Libraries: Scikit-learn, Matplotlib, DTAIDistance
- Special thanks to the Open Source and IoT communities

## LIVE DEMO HERE

-  https://crop-recommendation-using-ai-ml.onrender.com/
