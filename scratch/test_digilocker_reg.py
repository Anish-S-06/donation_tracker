import sys, os
sys.path.insert(0, os.path.abspath('.'))
from app import create_app, db
from app.models import User

app = create_app()
with app.test_client() as client:
    # 1. Test GET /auth/register
    res = client.get('/auth/register')
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert 'Verify with DigiLocker' in html, 'DigiLocker button not found'
    assert 'name="id_document"' not in html, 'id_document file input should be removed for community user'
    print('Test 1 Passed: Register page renders DigiLocker button and no id_document file upload')

    # 2. Test registration without DigiLocker verification (should block)
    res = client.post('/auth/register', data={
        'email': 'dl_test_unverified@example.com',
        'password': 'Password123!',
        'role': 'user',
        'digilocker_verified': '0'
    }, follow_redirects=True)
    html = res.data.decode('utf-8')
    assert 'DigiLocker verification is required' in html or 'Please verify' in html
    print('Test 2 Passed: Registration blocks unverified submissions')

    # 3. Test registration WITH DigiLocker verification
    res = client.post('/auth/register', data={
        'email': 'dl_verified_user@example.com',
        'password': 'Password123!',
        'role': 'user',
        'digilocker_verified': '1',
        'digilocker_doc_type': 'Aadhaar',
        'digilocker_doc_id': 'XXXX-XXXX-4819',
        'digilocker_name': 'Test Citizen'
    }, follow_redirects=False)
    assert res.status_code == 302
    assert '/verify-email-otp' in res.headers['Location']
    print('Test 3 Passed: Registration accepts DigiLocker verification and redirects to OTP')

    # 4. Complete OTP verification
    from app.core.auth_routes import otp_store
    otp = otp_store['dl_verified_user@example.com']['otp']
    res_otp = client.post('/auth/verify-email-otp', data={'otp': otp}, follow_redirects=True)
    assert res_otp.status_code == 200
    
    # 5. Check user in database
    with app.app_context():
        user = User.query.filter_by(email='dl_verified_user@example.com').first()
        assert user is not None
        assert user.verification_status == 'approved', f'Expected approved, got {user.verification_status}'
        assert 'DigiLocker Verified' in user.id_document
        print(f'Test 4 Passed: User auto-approved with status={user.verification_status}, id_document={user.id_document}')
        
        # Cleanup test user
        db.session.delete(user)
        db.session.commit()
        print('All DigiLocker registration tests passed successfully!')
