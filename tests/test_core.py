from app.models import Resource, User
from app import db

def test_create_resource(client, init_database):
    # Test POST /resources/
    response = client.post('/resources/', json={
        'donor_id': init_database.id,
        'title': 'Used Laptop',
        'description': 'A laptop in working condition',
        'category': 'Electronics',
        'condition': 'Good'
    })
    assert response.status_code == 201
    
    data = response.get_json()
    assert 'resource_id' in data

def test_get_resources(client, init_database):
    # Test GET /resources/
    resource = Resource(donor_id=init_database.id, title='Math Textbook', description='...', category='Books', condition='New')
    db.session.add(resource)
    db.session.commit()

    response = client.get('/resources/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert data[0]['title'] == 'Math Textbook'

def test_points_transaction(client, init_database):
    # Test POST /points/transaction
    response = client.post('/points/transaction', json={
        'user_id': init_database.id,
        'amount': 250,
        'transaction_type': 'Earned'
    })
    assert response.status_code == 201
    
    # Check if balance and badge updated correctly
    user = db.session.get(User, init_database.id)
    assert user.points_balance == 250
    assert user.badge_level == 'Silver'

def test_export_history(client, init_database):
    # Test GET /history/export
    response = client.get('/history/export')
    assert response.status_code == 200
    assert 'text/csv' in response.headers['Content-Type']
    assert response.headers['Content-Disposition'] == 'attachment;filename=donation_history.csv'
