from flask import render_template,request,session, redirect, url_for, flash
from app import app, db
from app.models import Product, Order , User ,OrderItem
from app.forms import AddProductForm ,RegistrationForm,LoginForm
from functools import wraps
from datetime import datetime


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Vérifier s'il y a déjà un admin
        existing_admin = User.query.filter_by(role='admin').first()
        role = 'admin' if not existing_admin else 'user'
        
        new_user = User(username=form.username.data, password=form.password.data, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Définition du décorateur
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route sécurisée par le décorateur login_required
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/products', methods=['GET', 'POST'])
@login_required
def manage_products():
    form = AddProductForm()

    # Filtrage
    search = request.args.get('search', '')
    min_quantity = request.args.get('min_quantity', None)
    max_quantity = request.args.get('max_quantity', None)

    # Tri
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')

    # Construire la requête
    products_query = Product.query

    if search:
        products_query = products_query.filter(Product.name.contains(search))

    if min_quantity:
        products_query = products_query.filter(Product.quantity >= int(min_quantity))

    if max_quantity:
        products_query = products_query.filter(Product.quantity <= int(max_quantity))

    # Appliquer le tri
    if sort_by == 'name':
        products_query = products_query.order_by(Product.name.asc() if sort_order == 'asc' else Product.name.desc())
    elif sort_by == 'quantity':
        products_query = products_query.order_by(Product.quantity.asc() if sort_order == 'asc' else Product.quantity.desc())
    elif sort_by == 'price':
        products_query = products_query.order_by(Product.price.asc() if sort_order == 'asc' else Product.price.desc())

    products = products_query.all()

    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            quantity=form.quantity.data,
            price=form.price.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('manage_products'))

    return render_template('products.html', products=products, form=form)

@app.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    if session.get('role') != 'admin':
        flash('You do not have permission to perform this action.')
        return redirect(url_for('manage_products'))
        
    product = Product.query.get_or_404(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!')
    else:
        flash('Product not found')  

    return redirect(url_for('manage_products'))



@app.route('/orders')
@login_required
def manage_orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddProductForm()

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        product.price = form.price.data
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('manage_products'))

    return render_template('edit_product.html', form=form, product=product)

@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    search_query = request.args.get('search', '')

    # Recherche de produits
    products = Product.query.filter(Product.name.contains(search_query)).all() if search_query else Product.query.all()

    if request.method == 'POST':
        try:
            # Créer une nouvelle commande
            order = Order(user_id=session['user_id'], total_price=0)
            db.session.add(order)
            db.session.commit()

            total_price = 0
            for item in request.form.getlist('products'):
                product_id, quantity = item.split(':')
                product = Product.query.get(product_id)
                quantity = int(quantity)

                if product and quantity > 0:
                    # Vérifier le stock et ajouter au total de la commande
                    item_total = product.price * quantity
                    if product.quantity < quantity:
                        flash(f'Not enough stock for {product.name}. Only {product.quantity} left.', 'danger')
                        return redirect(url_for('create_order'))

                    product.quantity -= quantity
                    order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, total_price=item_total)
                    db.session.add(order_item)

                    total_price += item_total

            order.total_price = total_price
            db.session.commit()

            flash(f'Order created successfully! Total: ${total_price:.2f}', 'success')
            return redirect(url_for('sales_history'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating order: {str(e)}', 'danger')
            return redirect(url_for('create_order'))

    return render_template('create_order.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if session.get('role') != 'admin':
        flash('You do not have permission to perform this action.')
        return redirect(url_for('index'))
    
    form = AddProductForm()
    
    if form.validate_on_submit():
        # Créez un produit avec les données validées par le formulaire
        new_product = Product(name=form.name.data, description=form.description.data, quantity=form.quantity.data, price=form.price.data)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('add_product'))  # Rester sur la page après l'ajout pour voir la liste mise à jour
    
    # Récupérer tous les produits existants pour les afficher sur la même page
    products = Product.query.all()

    return render_template('products.html', form=form, products=products)




@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))

    # Récupérer les informations du produit
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('create_order'))

    # Récupérer ou initialiser le panier dans la session
    cart = session.get('cart', [])
    
    # Ajouter l'article au panier
    cart.append({'product_id': product.id, 'name': product.name, 'price': product.price, 'quantity': quantity})
    session['cart'] = cart

    flash(f'{quantity} x {product.name} added to your order', 'success')
    return redirect(url_for('create_order'))

@app.route('/finalize_order', methods=['POST'])
@login_required
def finalize_order():
    cart = session.get('cart', [])

    if not cart:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('create_order'))

    # Liste pour stocker les messages d'erreur
    stock_errors = []

    # Vérifier le stock de chaque produit avant de créer la commande
    for item in cart:
        product = Product.query.get(item['product_id'])
        quantity = item['quantity']

        # Si la quantité demandée dépasse la quantité en stock, ajouter un message d'erreur
        if product.quantity < quantity:
            stock_errors.append(f'Not enough stock for {product.name}. Only {product.quantity} left.')

    # Si des erreurs de stock existent, les afficher et empêcher la finalisation de la commande
    if stock_errors:
        for error in stock_errors:
            flash(error, 'danger')
        return redirect(url_for('create_order'))

    # Si pas d'erreurs de stock, créer la commande
    order = Order(user_id=session['user_id'], total_price=0)
    db.session.add(order)
    db.session.commit()

    total_price = 0

    # Ajouter les items à la commande et mettre à jour le stock
    for item in cart:
        product = Product.query.get(item['product_id'])
        quantity = item['quantity']

        # Mettre à jour le stock
        product.quantity -= quantity

        # Calculer le prix total pour l'article
        item_total = product.price * quantity
        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, total_price=item_total)
        db.session.add(order_item)
        total_price += item_total

    # Mettre à jour le prix total de la commande
    order.total_price = total_price
    db.session.commit()

    # Vider le panier après la finalisation de la commande
    session.pop('cart', None)

    flash(f'Order created successfully! Total: ${total_price:.2f}', 'success')
    return redirect(url_for('sales_history'))


@app.route('/decrease_product/<int:product_id>', methods=['POST'])
@login_required
def decrease_product(product_id):
    if session.get('role') != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('manage_products'))
    
    product = Product.query.get_or_404(product_id)
    
    decrease_amount = int(request.form.get('decrease_amount', 1))  # Récupère la quantité à diminuer du formulaire, par défaut 1
    
    if decrease_amount <= 0:
        flash('Decrease amount must be positive.', 'danger')
        return redirect(url_for('manage_products'))
    
    if product.quantity >= decrease_amount:
        product.quantity -= decrease_amount
        db.session.commit()
        flash(f'{decrease_amount} units removed from {product.name}.', 'success')
    else:
        flash(f'Not enough stock to decrease {decrease_amount} units from {product.name}.', 'danger')
    
    return redirect(url_for('manage_products'))



@app.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))  # Récupère la quantité du formulaire
    product = Product.query.get_or_404(product_id)

    # Logique pour mettre à jour le panier
    cart = session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] = quantity
    else:
        cart[product_id] = {'name': product.name, 'price': product.price, 'quantity': quantity}

    # Sauvegarde le panier dans la session
    session['cart'] = cart
    session.modified = True

    flash(f'Cart updated for {product.name}', 'success')
    return redirect(url_for('view_cart'))


@app.route('/update_order_item/<int:order_item_id>', methods=['POST'])
@login_required
def update_order_item(order_item_id):
    order_item = OrderItem.query.get_or_404(order_item_id)
    new_quantity = int(request.form['new_quantity'])

    if new_quantity <= 0:
        flash('Quantity must be greater than zero.', 'danger')
        return redirect(url_for('sales_history'))

    product = Product.query.get(order_item.product_id)

    # Vérifier si la nouvelle quantité est disponible
    if new_quantity > product.quantity + order_item.quantity:
        flash(f'Not enough stock available for {product.name}.', 'danger')
        return redirect(url_for('sales_history'))

    # Ajuster le stock en fonction de la nouvelle quantité
    product.quantity += order_item.quantity  # Rendre la quantité actuelle au stock
    product.quantity -= new_quantity  # Soustraire la nouvelle quantité

    # Mettre à jour la quantité et le prix total
    order_item.quantity = new_quantity
    order_item.total_price = new_quantity * product.price
    db.session.commit()

    flash('Order item updated successfully.', 'success')
    return redirect(url_for('sales_history'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])

    # Vérifier si le produit est dans le panier
    updated_cart = [item for item in cart if item['product_id'] != product_id]
    
    if len(cart) == len(updated_cart):
        flash('Product not found in your cart', 'danger')
    else:
        session['cart'] = updated_cart
        flash('Product removed from your cart', 'success')
    
    return redirect(url_for('create_order'))


@app.route('/sales_history')
@login_required
def sales_history():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.timestamp.desc()).all()
    return render_template('sales_history.html', orders=orders)

@app.route('/low_stock_alerts')
def low_stock_alerts():
    threshold = 50  # Le seuil
    low_stock_products = Product.query.filter(Product.quantity <= threshold).all()
    return render_template('low_stock_alerts.html', products=low_stock_products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

