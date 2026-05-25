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
        # Create a dummy user if none exists
        if not User.query.get(1):
            dummy = User(id=1, email='prototype@example.com', password_hash='hash', role='donor')
            db.session.add(dummy)
            db.session.commit()
            print("Seeded dummy user for prototype.")

if __name__ == '__main__':
    seed_db()
    app.run(debug=True, use_reloader=False)
