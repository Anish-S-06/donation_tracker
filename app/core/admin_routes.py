from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Resource, Request
from app.core.decorators import role_required

admin_bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    # Fetch all users to display in the management table
    users = User.query.all()
    
    # Calculate some quick KPI metrics
    kpis = {
        'total_users': User.query.count(),
        'total_resources': Resource.query.count(),
        'pending_requests': Request.query.filter_by(status='Pending').count(),
        'fulfilled_donations': Request.query.filter_by(status='Fulfilled').count(),
    }
    
    return render_template('admin_dashboard.html', users=users, kpis=kpis)

@admin_bp.route('/users/<int:user_id>/verify', methods=['POST'])
@login_required
@role_required('admin')
def verify_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))
    if user.role == 'admin':
      flash('Admin accounts cannot be banned.','danger')
      return redirect(url_for('admin_routes.dashboard'))    
    
    user.is_verified = True
    user.verification_status='approved'
    db.session.commit()
    flash(f"{user.role.capitalize()} {user.email} verified successfully!", 'success')
    return redirect(url_for('admin_routes.dashboard'))

@admin_bp.route('/users/<int:user_id>/reject', methods=['POST'])
@login_required
@role_required('admin')
def reject_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))

    user.verification_status = 'rejected'
    user.is_verified = False

    db.session.commit()

    flash(f"{user.role.capitalize()} {user.email} rejected.", 'warning')
    return redirect(url_for('admin_routes.dashboard'))
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
    db.session.commit()
    flash(f"User {user.email} has been banned.", 'warning')
    return redirect(url_for('admin_routes.dashboard'))

@admin_bp.route('/users/<int:user_id>/unban', methods=['POST'])
@login_required
@role_required('admin')
def unban_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_routes.dashboard'))
        
    user.is_banned = False
    db.session.commit()
    flash(f"User {user.email} has been unbanned.", 'success')
    return redirect(url_for('admin_routes.dashboard'))

@admin_bp.route('/analytics/data')
@login_required
@role_required('admin')
def analytics_data():
    # User roles breakdown
    donor_count = User.query.filter_by(role='donor').count()
    receiver_count = User.query.filter_by(role='receiver').count()
    admin_count = User.query.filter_by(role='admin').count()
    
    # Resource status breakdown
    avail_count = Resource.query.filter_by(status='Available').count()
    req_count = Resource.query.filter_by(status='Requested').count()
    ful_count = Resource.query.filter_by(status='Fulfilled').count()
    
    # Listings by category
    categories = db.session.query(Resource.category, db.func.count(Resource.id))\
        .group_by(Resource.category).all()
        
    category_labels = [c[0] for c in categories]
    category_counts = [c[1] for c in categories]
    
    # If no resources exist, provide default categories for placeholder chart aesthetics
    if not category_labels:
        category_labels = ['Clothing', 'Food', 'Electronics', 'Books']
        category_counts = [0, 0, 0, 0]

    return jsonify({
        'users': {
            'labels': ['Donors', 'Receivers', 'Admins'],
            'data': [donor_count, receiver_count, admin_count]
        },
        'resources': {
            'labels': ['Available', 'Requested', 'Fulfilled'],
            'data': [avail_count, req_count, ful_count]
        },
        'categories': {
            'labels': category_labels,
            'data': category_counts
        }
    })
