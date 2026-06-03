from app import create_app, db
from app.models import User, Resource, Request, DonationHistory, PointsTransaction

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Resource': Resource,
        'Request': Request,
        'DonationHistory': DonationHistory,
        'PointsTransaction': PointsTransaction
    }

def seed_db():
    with app.app_context():
        db.create_all()
        
        # Seed an Admin User
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin_user = User(
                email='admin@example.com',
                role='admin',
                is_email_verified=True,
                is_phone_verified=True,
                is_verified=True
            )
            admin_user.set_password('adminpass')
            db.session.add(admin_user)
            print("Seeded Admin user (admin@example.com / adminpass)")

        # Seed a Donor User (Verified)
        donor = User.query.filter_by(email='donor@example.com').first()
        if not donor:
            donor_user = User(
                email='donor@example.com',
                role='donor',
                is_email_verified=True,
                is_phone_verified=True,
                is_verified=True
            )
            donor_user.set_password('donorpass')
            db.session.add(donor_user)
            print("Seeded Verified Donor user (donor@example.com / donorpass)")

        # Seed a Receiver User
        receiver = User.query.filter_by(email='receiver@example.com').first()
        if not receiver:
            receiver_user = User(
                email='receiver@example.com',
                role='receiver',
                is_email_verified=True,
                is_phone_verified=True,
                is_verified=True
            )
            receiver_user.set_password('receiverpass')
            db.session.add(receiver_user)
            print("Seeded Receiver user (receiver@example.com / receiverpass)")

        db.session.commit()

if __name__ == '__main__':
    seed_db()
    app.run(debug=True, use_reloader=False)
