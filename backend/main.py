from backend.config import config
import backend.database as database
from flask import Flask, request, jsonify, session, Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)
db = database.Database().get()

@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_seller:
            return redirect(url_for('main.admin_page'))
        return redirect(url_for('main.profile'))
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.email, specialSellerMessage="\nAdmin is logged in." if current_user.is_seller else "")

@main.route('/admin')
@login_required
def admin_page():
    if current_user.is_seller:
        return render_template('admin.html')
    return redirect(url_for('main.profile'))

@main.route('/cart')
@login_required
def cart():
    if current_user.is_seller:
        return redirect(url_for(main.admin_page))
    return render_template('cart.html')
