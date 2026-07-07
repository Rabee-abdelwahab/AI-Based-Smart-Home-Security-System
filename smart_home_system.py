import joblib
import pandas as pd

# ترتيب الـ Features (مهم جدًا)
FEATURES = [
    'Hour','Day','LDR','PIR_Living','PIR_Bedroom','PIR_Kitchen',
    'PIR_Bathroom','Temp_Living','Temp_Bedroom','Gas_Kitchen',
    'Gas_Bathroom','Flame','Soil_Moisture','Water_Level'
]

class SmartHomeSystem:

    def __init__(self):
        # تحميل الموديلات
        self.energy_model = joblib.load("energy_model.pkl")
        self.fire_model = joblib.load("fire_model.pkl")
        self.irrig_model = joblib.load("irrig_model.pkl")
        self.pool_model = joblib.load("pool_model.pkl")

    def predict(self, sensor_data):
        # تحويل البيانات إلى DataFrame
        sensor_df = pd.DataFrame([sensor_data], columns=FEATURES)

        # =========================
        # 🔋 Energy Prediction
        # =========================
        energy = self.energy_model.predict(sensor_df)[0]

        # تأثير الحرارة (Rule-based)
        temp_living = sensor_df["Temp_Living"].values[0]
        temp_bedroom = sensor_df["Temp_Bedroom"].values[0]

        if temp_living > 30:
            energy += 0.02

        if temp_bedroom > 30:
            energy += 0.02

        # =========================
        # 🔥 Fire Prediction
        # =========================
        fire = self.fire_model.predict(sensor_df)[0]

        flame = sensor_df["Flame"].values[0]
        pir_kitchen = sensor_df["PIR_Kitchen"].values[0]

        # لو في نار + حركة في المطبخ → طبخ مش حريق
        if flame == 1 and pir_kitchen == 1:
            fire = 0

        # =========================
        # 🌱 Irrigation
        # =========================
        irrigation = self.irrig_model.predict(sensor_df)[0]

        # =========================
        # 🏊 Pool
        # =========================
        pool = self.pool_model.predict(sensor_df)[0]

        # =========================
        # 📊 Output
        # =========================
        return {
            "Energy_kWh": float(energy),
            "Fire_Risk": int(fire),
            "Irrigation": int(irrigation),
            "Pool_Refill": int(pool)
        }


# =========================
# 🧪 Test Run
# =========================
if __name__ == "__main__":

    system = SmartHomeSystem()

    test_data = [
        14, 3, 300,   # Hour, Day, LDR
        1, 0, 1, 0,   # PIR (في حركة في المطبخ)
        35, 33,       # حرارة عالية
        200, 180,     # Gas
        1,            # Flame (في نار)
        40,           # Soil
        70            # Water
    ]

    result = system.predict(test_data)

    print("Smart Home Decision:")
    print(result)