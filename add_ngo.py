from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check if dummy NGO already exists
    existing = User.query.filter_by(email='help@dummyngo.org').first()
    if not existing:
        dummy_ngo = User(
            email='help@dummyngo.org',
            role='receiver', # or donor, doesn't matter for the splash screen
            is_ngo=True,
            ngo_name='Global Heart Foundation',
            ngo_description='Providing meals, clothing, and shelter to those in need across the community.',
            upi_id='globalheart@upi',
            verification_status='approved',
            is_email_verified=True
        )
        dummy_ngo.set_password('password123')
        db.session.add(dummy_ngo)
        db.session.commit()
        print("Successfully created dummy NGO: Global Heart Foundation!")
    else:
        print("Dummy NGO already exists.")
