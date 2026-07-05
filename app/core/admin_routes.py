from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Resource, Request as DonationRequest
from app.core.decorators import role_required

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')


# ======================================================
# ADMIN DASHBOARD
# ======================================================
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():

    users = User.query.filter_by(is_email_verified=True).all()

    kpis = {
        'total_users': User.query.count(),
        'total_resources': Resource.query.count(),
        'pending_requests': DonationRequest.query.filter_by(status='Pending').count(),
        'fulfilled_donations': DonationRequest.query.filter_by(status='Fulfilled').count(),
    }

    return render_template('admin_dashboard.html', users=users, kpis=kpis)


# ======================================================
# VERIFY USER (ADMIN APPROVAL)
# ======================================================
@admin_bp.route('/users/<int:user_id>/verify', methods=['POST'])
@login_required
@role_required('admin')
def verify_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    if user.role == 'admin':
        flash('Admin accounts cannot be modified.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    if user.is_banned:
        flash('Cannot verify a banned user.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    # ✅ ONLY admin approval
    user.verification_status = 'approved'

    db.session.commit()

    flash(f"{user.role.capitalize()} {user.email} verified successfully!", 'success')
    return redirect(url_for('admin_routes.dashboard'))


# ======================================================
# REJECT USER
# ======================================================
@admin_bp.route('/users/<int:user_id>/reject', methods=['POST'])
@login_required
@role_required('admin')
def reject_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    if user.role == 'admin':
        flash('Admin accounts cannot be modified.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    user.verification_status = 'rejected'

    db.session.commit()

    flash(f"{user.role.capitalize()} {user.email} rejected.", 'warning')
    return redirect(url_for('admin_routes.dashboard'))


# ======================================================
# BAN USER
# ======================================================
@admin_bp.route('/users/<int:user_id>/ban', methods=['POST'])
@login_required
@role_required('admin')
def ban_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    if user.id == current_user.id:
        flash('You cannot ban yourself!', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    user.is_banned = True

    # optional safety reset
    user.verification_status = 'rejected'

    db.session.commit()

    flash(f"User {user.email} has been banned.", 'warning')
    return redirect(url_for('admin_routes.dashboard'))


# ======================================================
# UNBAN USER
# ======================================================
@admin_bp.route('/users/<int:user_id>/unban', methods=['POST'])
@login_required
@role_required('admin')
def unban_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    user.is_banned = False

    # reset to pending after unban (recommended)
    user.verification_status = 'pending'

    db.session.commit()

    flash(f"User {user.email} has been unbanned.", 'success')
    return redirect(url_for('admin_routes.dashboard'))


# ======================================================
# ANALYTICS
# ======================================================
@admin_bp.route('/analytics/data')
@login_required
@role_required('admin')
def analytics_data():

    user_count = User.query.filter_by(role='user').filter_by(is_ngo=False).count()
    ngo_count = User.query.filter_by(is_ngo=True).count()
    admin_count = User.query.filter_by(role='admin').count()

    avail_count = Resource.query.filter_by(status='Available').count()
    req_count = Resource.query.filter_by(status='Requested').count()
    ful_count = Resource.query.filter_by(status='Fulfilled').count()

    categories = db.session.query(
        Resource.category,
        db.func.count(Resource.id)
    ).group_by(Resource.category).all()

    labels = [c[0] for c in categories]
    values = [c[1] for c in categories]

    if not labels:
        labels = ['Clothing', 'Food', 'Electronics', 'Books']
        values = [0, 0, 0, 0]

    return jsonify({
        'users': {
            'labels': ['Community Users', 'NGOs', 'Admins'],
            'data': [user_count, ngo_count, admin_count]
        },
        'resources': {
            'labels': ['Available', 'Requested', 'Fulfilled'],
            'data': [avail_count, req_count, ful_count]
        },
        'categories': {
            'labels': labels,
            'data': values
        }
    })