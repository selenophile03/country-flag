import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class CountryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.country_label = QLabel("Enter Country Name : ", self)
        self.country_input = QLineEdit(self)
        self.button = QPushButton("Get Info", self)
        self.capital = QLabel("", self)
        self.time = QLabel("", self)
        self.lang = QLabel("", self)
        self.currency = QLabel("", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Country App")
        self.resize(500, 500) 

        vbox = QVBoxLayout()
        vbox.addWidget(self.country_label)
        vbox.addWidget(self.country_input)
        vbox.addWidget(self.button)
        vbox.addWidget(self.capital)
        vbox.addWidget(self.time)
        vbox.addWidget(self.lang)
        vbox.addWidget(self.currency)

        self.setLayout(vbox)
        self.country_label.setAlignment(Qt.AlignCenter)
        self.country_input.setAlignment(Qt.AlignCenter)
        self.capital.setAlignment(Qt.AlignCenter)
        self.time.setAlignment(Qt.AlignCenter)
        self.lang.setAlignment(Qt.AlignCenter)
        self.currency.setAlignment(Qt.AlignCenter)

        self.capital.setWordWrap(True)
        self.time.setWordWrap(True)
        self.lang.setWordWrap(True)
        self.currency.setWordWrap(True)

        self.country_label.setObjectName("Country")
        self.country_input.setObjectName("Input")
        self.button.setObjectName("Button")
        self.capital.setObjectName("Capital")
        self.time.setObjectName("Time")
        self.lang.setObjectName("Lang")
        self.currency.setObjectName("Currency")

        self.setStyleSheet("""
            QWidget{
                background-color: black;
            }
            QLabel{
                font-size: 24px;
                font-family : Times New Roman;
                color: red;
            }
            QLabel#Country{
                font-size: 36px;
                font-family : Times New Roman;
                color: red;
                font-weight: bold;
            }
            QLineEdit#Input{
                font-size: 28px;
                font-family : Times New Roman;
                color: orange;
            }
            QPushButton#Button{
                font-size: 28px;
                font-family : Times New Roman;
                color: white;
                font-style: italic;           
            }
            QLabel#Capital{
                font-size: 32px;
                font-family : Times New Roman;
                color: violet;
                font-weight: bold;
            }
            QLabel#Time{
                font-size: 28px;
                font-family : Segoe UI Emoji;
                color: cyan;            
            }
            QLabel#Lang{
                font-size: 28px;
                font-family : Times New Roman;
                color: white;
                font-style: italic;                
            }
            QLabel#Currency{
                font-size: 28px;
                font-family : Times New Roman;
                color: yellow;
                font-weight: bold;            
            }
        """)

        self.button.clicked.connect(self.get_info)

    def get_info(self):
        country_name = self.country_input.text().strip()
        if not country_name:
            self.capital.setText("Please enter a country name")
            return

        try:
            url = f"https://restcountries.com{country_name}"
            response = requests.get(url, timeout=5) 

            if response.status_code == 200:
                data = response.json()
                self.info(data[0]) 
            else:
                self.capital.setText("Country not found!")
                self.time.setText("")
                self.lang.setText("")
                self.currency.setText("")

        except requests.exceptions.RequestException:
            self.capital.setText("Network error connection issue.")
            self.time.setText("")
            self.lang.setText("")
            self.currency.setText("")
        except Exception:
            self.capital.setText("Error processing data.")

    def info(self, country_data):
        capitals = country_data.get("capital", ["N/A"])
        capital_str = ", ".join(capitals)
        self.capital.setText(f"Capital: {capital_str}")

        timezones = country_data.get("timezones", ["N/A"])
        timezone_str = ", ".join(timezones)
        self.time.setText(f"Timezone: {timezone_str}")

        languages = country_data.get("languages", {})
        lang_str = ", ".join(languages.values()) if languages else "N/A"
        self.lang.setText(f"Languages: {lang_str}")

        currencies = country_data.get("currencies", {})
        curr_list = []
        for code, details in currencies.items():
            curr_name = details.get("name", code)
            curr_symbol = details.get("symbol", "")
            curr_list.append(f"{curr_name} ({curr_symbol})" if curr_symbol else curr_name)
        curr_str = ", ".join(curr_list) if curr_list else "N/A"
        self.currency.setText(f"Currency: {curr_str}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    country = CountryApp()
    country.show()
    sys.exit(app.exec_())

