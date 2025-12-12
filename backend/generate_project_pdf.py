
import sys
import subprocess
import os

# Install fpdf if not present
try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])
    from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        self.cell(0, 10, 'Laptop Price Prediction - Project Documentation', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

def create_pdf():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Project Overview
    pdf.chapter_title('1. Project Overview')
    pdf.chapter_body(
        "This project is a Full-Stack Web Application used to predict laptop prices based on various "
        "hardware specifications. It uses a Machine Learning model trained on historical data, "
        "served via a Flask backend, and presented through a modern, responsive frontend."
    )

    # Backend Files
    pdf.chapter_title('2. Backend Core (Python/Flask)')
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'app.py', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- The heart of the application.\n"
        "- Initializes the Flask web server.\n"
        "- Connects to the SQLite database (SQLAlchemy).\n"
        "- Loads ML models (pickle) at startup.\n"
        "- Defines API Routes:\n"
        "  * /predict: Receives data, scales it, runs model, returns price.\n"
        "  * /auth routes: Handles Login, Signup, OTP verification.\n"
        "  * /history: Fetches user's past predictions."
    )
    pdf.ln()

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'otp_config.py', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- Stores sensitive configuration for the OTP system.\n"
        "- Contains SMTP credentials (for email sending) and expiry time settings."
    )
    pdf.ln()

    # Database
    pdf.chapter_title('3. Database & Storage')
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'instance/laptop_price.db', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- A binary SQLite database file.\n"
        "- Stores structured data in tables: Users, Predictions, OTPs.\n"
        "- Lightweight, serverless database ideal for this application."
    )
    pdf.ln()

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'view_database.py', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- A custom utility script created for administration.\n"
        "- Connects to the .db file and prints readable tables to the console.\n"
        "- Useful for debugging and verifying data storage."
    )
    pdf.ln()

    # Machine Learning
    pdf.chapter_title('4. Machine Learning Assets')
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'model.pkl, encoder.pkl, scaler.pkl', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- model.pkl: The serialized Machine Learning regressor model.\n"
        "- encoder.pkl: Converts categorical text (e.g., 'Dell', 'HP') into numbers.\n"
        "- scaler.pkl: Standardizes numerical inputs (RAM, Weight) to match training scale."
    )
    pdf.ln()

    # Frontend
    pdf.chapter_title('5. Frontend (User Interface)')

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'templates/landing.html', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- The 'Welcome' page.\n"
        "- Features animations and 'Get Started' call-to-action.\n"
        "- Designed to impress users immediately."
    )
    pdf.ln()

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'templates/index.html', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- The main dashboard.\n"
        "- Contains the prediction form (Brand, RAM, CPU, etc.).\n"
        "- Displays the Price Prediction History table."
    )
    pdf.ln()

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'static/js/app.js', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 5, 
        "- Handles client-side logic.\n"
        "- Validates form inputs before sending.\n"
        "- Makes asynchronous (AJAX) calls to the Flask backend.\n"
        "- Dynamically updates the UI with the predicted price without reloading."
    )
    pdf.ln()

    # Save
    filename = "Laptop_Price_Prediction_Presentation.pdf"
    pdf.output(filename)
    print(f"PDF generated successfully: {filename}")

if __name__ == "__main__":
    create_pdf()
