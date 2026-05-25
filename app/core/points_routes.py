from flask import jsonify, request
from . import points_bp
from app.models import User, PointsTransaction
from app import db

@points_bp.route('/balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'user_id': user.id,
        'points_balance': user.points_balance,
        'trust_score': user.trust_score,
        'badge_level': user.badge_level
    }), 200

@points_bp.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.json
    if not data or not all(k in data for k in ('user_id', 'amount', 'transaction_type')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    amount = int(data['amount'])
    transaction_type = data['transaction_type'] # 'Earned' or 'Spent'
    
    # Validation logic
    if transaction_type == 'Spent' and user.points_balance < amount:
        return jsonify({'error': 'Insufficient points balance'}), 400
        
    new_txn = PointsTransaction(
        user_id=user.id,
        amount=amount,
        transaction_type=transaction_type,
        description=data.get('description', '')
    )
    db.session.add(new_txn)
    
    # Update balance
    if transaction_type == 'Earned':
        user.points_balance += amount
    else:
        user.points_balance -= amount
        
    # Badging logic threshold based on total points
    if user.points_balance >= 1000:
        user.badge_level = 'Platinum'
    elif user.points_balance >= 500:
        user.badge_level = 'Gold'
    elif user.points_balance >= 200:
        user.badge_level = 'Silver'
    elif user.points_balance >= 50:
        user.badge_level = 'Bronze'
        
    db.session.commit()
    
    return jsonify({
        'message': 'Transaction recorded successfully',
        'new_balance': user.points_balance,
        'new_badge': user.badge_level
    }), 201
