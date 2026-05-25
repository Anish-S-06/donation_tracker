import csv
from io import StringIO
from flask import jsonify, Response
from . import history_bp
from app.models import DonationHistory, Request
from app import db

@history_bp.route('/user/<int:user_id>', methods=['GET'])
def get_history(user_id):
    # Get history where the user is either the donor or receiver
    # We join with the Request table to find the users involved
    histories = DonationHistory.query.join(Request).filter(
        (Request.receiver_id == user_id) | (Request.resource.has(donor_id=user_id))
    ).all()
    
    result = []
    for h in histories:
        result.append({
            'id': h.id,
            'request_id': h.request_id,
            'completed_at': h.completed_at,
            'donor_rating': h.donor_rating,
            'receiver_rating': h.receiver_rating,
            'resource_title': h.request.resource.title
        })
    return jsonify(result), 200

@history_bp.route('/export', methods=['GET'])
def export_csv():
    # Export all history as CSV
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['History ID', 'Request ID', 'Resource Title', 'Donor ID', 'Receiver ID', 'Completed At', 'Donor Rating', 'Receiver Rating'])
    
    records = DonationHistory.query.join(Request).all()
    for r in records:
        cw.writerow([
            r.id,
            r.request_id,
            r.request.resource.title,
            r.request.resource.donor_id,
            r.request.receiver_id,
            r.completed_at,
            r.donor_rating,
            r.receiver_rating
        ])
        
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=donation_history.csv"}
    )
