# EB Calculator Pro - Django MongoDB Project

A comprehensive electricity bill calculator web application built with Django and MongoDB, specifically designed for Tamil Nadu EB (Electricity Board) tariff calculations.

## Features

- **User Authentication**: Secure user registration and login system
- **Daily Usage Tracking**: Track daily electricity consumption by appliances
- **Tamil Nadu EB Tariff**: Accurate bi-monthly bill calculation using official tariff slabs
- **MongoDB Integration**: All data stored in MongoDB for scalability
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Calculations**: Instant bill calculations with detailed breakdowns

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MongoDB with MongoEngine ODM
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with modern design patterns
- **Authentication**: Custom session-based authentication

## Prerequisites

1. **Python 3.8+**
2. **MongoDB** (Community Edition)
3. **pip** (Python package manager)

## Installation

### 1. Clone or Download the Project
```bash
# If you have the project files, navigate to the project directory
cd "Downloads\final python"
```

### 2. Install MongoDB
- **Windows**: Download from [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- **macOS**: `brew install mongodb-community`
- **Linux**: `sudo apt-get install mongodb`

### 3. Start MongoDB
```bash
# Windows (if installed as service, it should start automatically)
mongod

# macOS/Linux
sudo systemctl start mongod
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run MongoDB Setup
```bash
python setup_mongodb.py
```
This will create a sample user and generate test data.

### 6. Import Existing Data (Optional)
If you have existing energy usage data:
```bash
python manage.py import_energy_data --username testuser --file "energyFILE (1).txt" --create-user
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
Open your browser and go to: `http://127.0.0.1:8000`

**Sample Login Credentials:**
- Username: `testuser`
- Password: `testpassword123`

## Usage

### 1. User Authentication
- Use the sample credentials above, or
- Navigate to the signup page to create a new account
- Password must be at least 8 characters with uppercase, lowercase, and special characters

### 2. Daily Usage Tracking
- Login to your dashboard
- Add daily electricity usage by selecting appliances
- Enter units consumed for each appliance
- Data is automatically saved to MongoDB

### 3. Bill Calculation

#### Option A: Auto Generate from Usage Data
- Click "Auto Generate from Usage Data" on the dashboard
- System automatically calculates total consumption for the last 2 months
- Generates bill using stored daily usage data

#### Option B: Manual Bill Entry
- Click "Manual Bill Entry"
- Enter previous and current meter readings
- Enter customer name
- The system automatically calculates using Tamil Nadu EB tariff slabs:
  - First 200 units: Free
  - 201-400 units: ₹2.25/unit
  - 401-500 units: ₹4.50/unit
  - 501-600 units: ₹6.00/unit
  - 601-800 units: ₹8.00/unit
  - 801-1000 units: ₹9.00/unit
  - Above 1000 units: ₹10.50/unit

### 4. Bill Features
- Detailed slab-wise breakdown
- Fixed charges and electricity duty calculation
- Printable invoice format
- Due date calculation

## Project Structure

```
Downloads\final python\
├── eb_calculator/          # Django project settings
│   ├── __init__.py
│   ├── settings.py         # MongoDB configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI application
├── bills/                 # Main Django app
│   ├── __init__.py
│   ├── admin.py           # Admin configuration
│   ├── apps.py            # App configuration
│   ├── forms.py           # Django forms
│   ├── models.py          # MongoDB models
│   ├── urls.py            # App URL routing
│   ├── utils.py           # Tamil Nadu tariff logic
│   └── views.py           # View functions
├── templates/bills/       # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── dashboard.html     # Main dashboard
│   ├── bill_calculator.html # Bill calculator
│   └── bill_invoice.html  # Bill invoice
├── static/css/           # CSS files
│   └── style.css         # Main stylesheet
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── setup.py             # Setup script
└── README.md            # This file
```

## MongoDB Collections

The application creates the following MongoDB collections:

1. **users**: User account information
2. **daily_usage**: Daily electricity usage records
3. **bill_calculations**: Generated bill records
4. **user_sessions**: User session management

## Tamil Nadu EB Tariff Implementation

The application implements the official Tamil Nadu EB domestic tariff structure:

- **Bi-monthly billing cycle** (2 months)
- **Slab-based pricing** with progressive rates
- **Fixed charges** based on consumption slabs
- **Electricity duty** at 15% of energy charges
- **Service charges** of ₹25

## Customization

### Adding New Appliances
Edit `templates/bills/dashboard.html` and add new options to the appliance dropdown.

### Modifying Tariff Rates
Update the `TARIFF_SLABS` in `bills/utils.py` to reflect any tariff changes.

### Styling Changes
Modify `static/css/style.css` for design customizations.

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod --version`
- Check if MongoDB service is started
- Verify connection settings in `eb_calculator/settings.py`

### Python Dependencies
- Use a virtual environment: `python -m venv venv`
- Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
- Install dependencies: `pip install -r requirements.txt`

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check `STATIC_URL` and `STATICFILES_DIRS` in settings

## Development

### Adding New Features
1. Create new models in `bills/models.py`
2. Add corresponding views in `bills/views.py`
3. Create templates in `templates/bills/`
4. Update URL routing in `bills/urls.py`

### Database Operations
Use MongoDB Compass or command line tools to inspect and manage data.

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use environment variables for sensitive settings
- Implement proper user input validation
- Add HTTPS in production

## License

This project is for educational and personal use. Please ensure compliance with local electricity board regulations when using tariff calculations.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify MongoDB is running
3. Ensure all dependencies are installed
4. Check Django logs for error details

## Future Enhancements

- PDF bill generation
- Email notifications
- Usage analytics and charts
- Mobile app integration
- Multiple tariff support (other states)
- Payment integration
