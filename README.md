# 🌾 Precision Agriculture using AI and Arduino

This project integrates **Artificial Intelligence (AI)** and **IoT using Arduino** to recommend the most suitable crops for a given field, based on real-time environmental data like soil moisture, pH, humidity, temperature, and more.

---

## 📌 Project Objective

To develop a **smart crop recommendation system** that collects real-time environmental data via sensors and uses a trained **Machine Learning model** to suggest the best crop to grow.

---

## 📦 Technologies Used

- Arduino Uno + Sensors (Soil Moisture, pH, MQ135, LDR, TMP36, Rain Sensor)
- Python (Data Processing, Visualization, ML)
- Machine Learning (Random Forest Classifier)
- Matplotlib, Pandas, Scikit-learn
- Dynamic Time Warping (DTW) for graph similarity

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

1. Connect Arduino with sensors and upload the Arduino code.
2. Run the Python script:
   ```bash
   python_folder_name.py
   ```
3. Serial data will be read and fed into the ML model.
4. The model will print the most suitable crop and show visual graphs.

---

## 📊 Graphical Analysis

- Real-time sensor readings are plotted.
- Spline interpolation smooths the graph.
- DTW compares new data with ideal crop profiles.
- Outputs similarity % and top matching crops.

---

## 📁 File Structure

```
📦 Project Root
├── recommendation.csv          # Dataset
├── main.py                     # Python ML & Graph code
├── arduino.ino                 # Arduino sketch
├── Precision_Agriculture_Report.pdf   # Final report
└── README.md                   # This file
```

---

## ✅ Results

- Model Accuracy: ~92%   
- Graph similarity scoring for decision confidence

---

## 🚀 Future Scope

- Mobile app with sensor integration  
- Smart irrigation automation  
- GPS-based location-aware suggestions  

---

## 📝 Credits

- Libraries: Scikit-learn, Matplotlib, DTAIDistance
- Special thanks to the Open Source and IoT communities
