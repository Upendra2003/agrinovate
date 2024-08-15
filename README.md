
# AgriInnovate

AgriInnovate is a Django-based project aimed at providing comprehensive agricultural data management and visualization. This project includes features for monitoring crop health, analyzing soil conditions, and integrating weather data for better agricultural decisions.

## Features

- **Dashboard:** A user-friendly interface to visualize crop health, soil conditions, weather data, and market trends.
- **Data Integration:** Connects to IoT devices for real-time soil data updates.
- **Analytics:** Provides tools for analyzing agricultural data to optimize crop yields.
- **REST API Integration:** Allows for seamless integration with external data sources.

## Installation

To set up and run this project locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Anuragreat/agrinovate.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd agrinovate
   ```

3. **Create a Virtual Environment:**
   ```bash
   python -m venv agri
   ```

4. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     .\agri\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source agri/bin/activate
     ```

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application:**
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

- **Dashboard:** Provides an overview of the crop health, soil conditions, and weather data.

