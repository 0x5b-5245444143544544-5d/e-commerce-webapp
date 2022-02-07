from backend.config import config
import backend.database as database
from flask import Flask, request, jsonify, session, Blueprint, render_template, redirect, url_for, flash
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
        cart_items = [item for item in db['orders'].all()]
        if not cart_items:
            return render_template('admin_nohistory.html')
        
        items = []
        for item in cart_items:
            items.append(dict(
                id = item['item_id'],
                item_name = db['items'].find_one(id=item['item_id'])['item_name'],
                order_quantity = item['order_quantity']
            ))
            
        total_items = len(items)
        items_perpage = 10
        
        current_page = request.args.get("page_no")
        
        if not current_page or not current_page.isnumeric():
            page_no = 1
        else:
            page_no = int(current_page)
        pages = int(total_items/items_perpage)+(1 if total_items%items_perpage!=0 else 0)
        if page_no<1 or page_no>pages:
            page_no = 1
        
        if page_no < pages:
            current_page_items = items[(page_no-1)*items_perpage: page_no*items_perpage]
        else:
            current_page_items = items[(pages-1)*items_perpage:]
        
        return render_template('admin.html', 
            len=len(current_page_items), 
            items=current_page_items, 
            previous_page_link=url_for("main.admin_page")+f"?page_no={page_no-1 if page_no > 1 else 1}", 
            next_page_link=url_for("main.admin_page")+f"?page_no={page_no+1 if page_no < pages else pages}")
    
    
    return redirect(url_for('main.profile'))

@main.route('/add_cart', methods=['POST'])
@login_required
def cart():
    order_item_id = int(request.form.get('order_button'))
    user_cart_item = db['cart'].find_one(user_id=int(current_user.id), item_id=order_item_id)
    if not user_cart_item:
        db['cart'].insert(dict(
            user_id=current_user.id,
            item_id=order_item_id,
            order_quantity=1
        ))
    else:
        user_cart_item['order_quantity']+=1
        db['cart'].update(user_cart_item, ['id'])
    
    orders_entry = db['orders'].find_one(item_id=order_item_id)
    if not orders_entry:
        db['orders'].insert(dict(
            item_id=order_item_id,
            order_quantity=1
        ))
    else:
        orders_entry['order_quantity']+=1
        db['orders'].update(orders_entry, ['id'])
    
    flash(f'Placed order for item: {order_item_id}')
    return redirect(url_for('main.items_page'))

@main.route('/items')
@login_required
def items_page():
    # get all items from DB
    items = [item for item in db['items'].find()]
    total_items = len(items)
    items_perpage = 10
    
    current_page = request.args.get("page_no")
    
    if not current_page or not current_page.isnumeric():
        page_no = 1
    else:
        page_no = int(current_page)
    pages = int(total_items/items_perpage)+(1 if total_items%items_perpage!=0 else 0)
    if page_no<1 or page_no>pages:
        page_no = 1
    
    if page_no < pages:
        current_page_items = items[(page_no-1)*items_perpage: page_no*items_perpage]
    else:
        current_page_items = items[(pages-1)*items_perpage:]
    
    return render_template('items.html', 
        len=len(current_page_items), 
        items=current_page_items, 
        previous_page_link=url_for("main.items_page")+f"?page_no={page_no-1 if page_no > 1 else 1}", 
        next_page_link=url_for("main.items_page")+f"?page_no={page_no+1 if page_no < pages else pages}")

@main.route('/cart_view')
@login_required
def cart_view():
    # get all items from DB
    cart_items = [item for item in db['cart'].find(user_id=current_user.id)]
    if not cart_items:
        return redirect(url_for('main.items_page'))
    
    items = []
    for item in cart_items:
        items.append(dict(
            id = item['item_id'],
            item_name = db['items'].find_one(id=item['item_id'])['item_name'],
            order_quantity = item['order_quantity']
        ))
        
    total_items = len(items)
    items_perpage = 10
    
    current_page = request.args.get("page_no")
    
    if not current_page or not current_page.isnumeric():
        page_no = 1
    else:
        page_no = int(current_page)
    pages = int(total_items/items_perpage)+(1 if total_items%items_perpage!=0 else 0)
    if page_no<1 or page_no>pages:
        page_no = 1
    
    if page_no < pages:
        current_page_items = items[(page_no-1)*items_perpage: page_no*items_perpage]
    else:
        current_page_items = items[(pages-1)*items_perpage:]
    
    return render_template('cart.html', 
        len=len(current_page_items), 
        items=current_page_items, 
        previous_page_link=url_for("main.cart_view")+f"?page_no={page_no-1 if page_no > 1 else 1}", 
        next_page_link=url_for("main.cart_view")+f"?page_no={page_no+1 if page_no < pages else pages}")