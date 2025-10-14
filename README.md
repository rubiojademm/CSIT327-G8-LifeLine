# LifeLine
A simple, centralized system that allows users to record meaningful life events and visualize them in a structured timeline by providing
an organized and interactive platform for logging experiences, visualizing personal progress, and encouraging continuous self-reflection and motivation.
## Installation
1. Clone the repository
2. Create virtual environment: `python -m venv env`
3. Activate environment: `source env/bin/activate` (Linux/Mac) or `env\Scripts\activate` 
(Windows)
4. Install requirements: `pip install -r requirements.txt`
5. Set up environment variables
     - Copy the example environment file: `cp .env.example .env`
     - Open .env and update the following:
       
        - Replace YOUR_PASSWORD with your Supabase database password
        - Replace < project-ref > with your Supabase project reference
       
7. Run migrations: `python manage.py migrate`
8. (Optional) Create superuser: `python manage.py createsuperuser`
9. Run server: `python manage.py runserver`
## Technology Stack
- Python/Django
- Supabase
- HTML/CSS/JavaScript
## Developers
- Jecie Jade Rubio, Full-stack developer, jeciejade.rubio@cit.edu
- Vince Raymund Alerta, Full-stack developer, vinceraymund.alerta@cit.edu
