# import os
# import sys
# import joblib
# import numpy as np
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
# )

# # Load the model safely using relative path
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS  # for PyInstaller
#     except AttributeError:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

# model_path = resource_path("svm_diabetes_model.pkl")
# model = joblib.load(model_path)

# class DiabetesApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Diabetes Class Predictor")

#         self.form_layout = QFormLayout()
#         self.inputs = {}

#         # Features
#         features = [
#             "Gender (0=M, 1=F)", "AGE", "Urea", "Cr", "HbA1c", "Chol",
#             "TG", "HDL", "LDL", "VLDL", "BMI"
#         ]
#         for feature in features:
#             inp = QLineEdit()
#             self.inputs[feature] = inp
#             self.form_layout.addRow(feature, inp)

#         self.predict_button = QPushButton("Predict")
#         self.predict_button.clicked.connect(self.predict)

#         self.result_label = QLabel("")
#         self.form_layout.addRow(self.predict_button)
#         self.form_layout.addRow(self.result_label)

#         self.setLayout(self.form_layout)

#     def predict(self):
#         try:
#             values = [float(self.inputs[f].text()) for f in self.inputs]
#             X = np.array(values).reshape(1, -1)
#             prediction = model.predict(X)[0]

#             class_map = {0: 'N', 1: 'P', 2: 'Y'}
#             result = class_map.get(prediction, "Unknown")

#             self.result_label.setText(f"Prediction: {result}")
#         except Exception as e:
#             QMessageBox.critical(self, "Error", str(e))

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DiabetesApp()
#     window.show()
#     sys.exit(app.exec_())

import os
import sys
import joblib
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QSlider, QRadioButton, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QButtonGroup, QVBoxLayout
)
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

model_path = resource_path("svm_diabetes_model.pkl")
model = joblib.load(model_path)

class DiabetesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diabetes Class Predictor")
        self.setFixedWidth(450)

        self.form_layout = QFormLayout()
        self.inputs = {}

        # Gender Radio Buttons
        self.gender_group = QButtonGroup(self)
        self.gender_male = QRadioButton("Male")
        self.gender_female = QRadioButton("Female")
        self.gender_male.setChecked(True)

        self.gender_group.addButton(self.gender_male, 0)
        self.gender_group.addButton(self.gender_female, 1)

        gender_layout = QHBoxLayout()
        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)
        self.form_layout.addRow("Gender:", gender_layout)

        # Sliders: original scale, since we apply log1p later
        # Values based on pre-log data to give user-friendly inputs
        slider_info = {
            "AGE":    (20, 79, 1, 55),      # Age (years)
            "Urea":   (0.5, 40.0, 0.1, 4.6),  # Urea (mg/dL)
            "Cr":     (6.0, 800.0, 1, 60),    # Creatinine (μmol/L or mg/dL)
            "HbA1c":  (0.9, 16.0, 0.1, 8.0),  # HbA1c (%)
            "Chol":   (0.0, 10.3, 0.1, 4.8),  # Cholesterol (mmol/L or mg/dL)
            "TG":     (0.3, 13.8, 0.1, 2.0),  # Triglycerides (mmol/L)
            "HDL":    (0.2, 9.9, 0.1, 1.1),   # HDL (mmol/L)
            "LDL":    (0.3, 9.9, 0.1, 2.5),   # LDL (mmol/L)
            "VLDL":   (0.1, 35.0, 0.1, 0.9),  # VLDL (mmol/L)
            "BMI":    (19.0, 47.8, 0.1, 30.0) # BMI (kg/m²)
        }

        # for feature, (min_val, max_val, scale, default_val) in slider_info.items():
        #     slider = QSlider(Qt.Horizontal)
        #     slider.setRange(int(min_val / scale), int(max_val / scale))
        #     slider.setValue(int(default_val / scale))
        #     slider_label = QLabel(f"{default_val:.1f}")
        #     slider.valueChanged.connect(lambda val, s=scale, l=slider_label: l.setText(f"{val * s:.1f}"))

        #     container = QVBoxLayout()
        #     container.addWidget(slider)
        #     container.addWidget(slider_label)

        #     self.inputs[feature] = (slider, scale)
        #     self.form_layout.addRow(f"{feature}:", container)

        from PyQt5.QtWidgets import QLineEdit

        def on_text_committed(box, slider, scale):
            text = box.text()
            try:
                num = float(text)
                slider.setValue(int(num / scale))
            except ValueError:
                pass  # Invalid input, ignore

        # Inside the loop
        for feature, (min_val, max_val, scale, default_val) in slider_info.items():
            slider = QSlider(Qt.Horizontal)
            slider.setRange(int(min_val / scale), int(max_val / scale))
            slider.setValue(int(default_val / scale))

            value_box = QLineEdit(f"{default_val:.1f}")
            value_box.setFixedWidth(60)

            # Sync: Slider → Text
            slider.valueChanged.connect(
                lambda val, s=scale, box=value_box: box.setText(f"{val * s:.1f}")
            )

            # Sync: Text → Slider (with validation)
            def on_text_changed(text, s=scale, sl=slider):
                try:
                    num = float(text)
                    sl.setValue(int(num / s))
                except ValueError:
                    pass  # ignore invalid input

            # value_box.textChanged.connect(on_text_changed)
            value_box.editingFinished.connect(lambda s=scale, box=value_box, sl=slider: on_text_committed(box, sl, s))

            container = QHBoxLayout()
            container.addWidget(slider)
            container.addWidget(value_box)

            self.inputs[feature] = (slider, scale, value_box)
            self.form_layout.addRow(f"{feature}:", container)

        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(self.predict)
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.form_layout.addRow(self.predict_button)
        self.form_layout.addRow("Result:", self.result_label)
        self.setLayout(self.form_layout)

    def predict(self):
        try:
            gender = self.gender_group.checkedId()
            values = [gender]

            # for feature in self.inputs:
            #     slider, scale = self.inputs[feature]
            for feature in self.inputs:
                slider, scale, _ = self.inputs[feature]
                raw_val = slider.value() * scale
                # Apply log1p transformation (skip for Gender)
                transformed_val = np.log1p(raw_val)
                values.append(transformed_val)

            X = np.array(values).reshape(1, -1)
            prediction = model.predict(X)[0]

            class_map = {
                0: ("Normal (N)", "#27ae60"),
                1: ("Prediabetes (P)", "#f39c12"),
                2: ("Diabetes (Y)", "#c0392b")
            }

            label, color = class_map.get(prediction, ("Unknown", "#7f8c8d"))
            self.result_label.setText(f"Prediction: {label}")
            self.result_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px;")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiabetesApp()
    window.show()
    sys.exit(app.exec_())