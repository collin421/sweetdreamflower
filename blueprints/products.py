from flask import Blueprint, request, render_template, redirect, url_for
from .func import get_db, generate_code

products_blueprint = Blueprint('products', __name__, template_folder='templates')

@products_blueprint.route('/products', methods=['GET', 'POST'])
def products():
    db = get_db()
    cur = db.cursor()

    sort_query = request.args.get('sort', 'id')
    filter_query = request.args.get('filter', '')

    # 정렬 쿼리 처리
    if sort_query == 'color':
        sort_query = 'color ASC'
    elif sort_query == 'bud_type':
        sort_query = 'bud_type ASC'
    elif sort_query == 'name desc':
        sort_query = 'name DESC'
    elif sort_query == 'name':
        sort_query = 'name ASC'

    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    if filter_query:
        cur.execute(f"SELECT * FROM products WHERE name LIKE ? ORDER BY {sort_query} LIMIT ? OFFSET ?", ('%' + filter_query + '%', per_page, offset))
    else:
        cur.execute(f"SELECT * FROM products ORDER BY {sort_query} LIMIT ? OFFSET ?", (per_page, offset))
    products = cur.fetchall()

    if request.method == 'POST':
        if 'delete' in request.form:
            product_id = request.form['delete']
            cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
            db.commit()
        elif 'product_name' in request.form and 'options' in request.form:
            product_name = request.form['product_name']
            options = request.form['options'].split(',')
            bud_type = request.form['bud_type']  # 꽃봉오리 타입 필드 추가

            for option in options:
                option = option.strip()
                if option:
                    product_code = generate_code(6)
                    cur.execute("INSERT INTO products (name, color, bud_type, code) VALUES (?, ?, ?, ?)", (product_name, option, bud_type, product_code))
                    db.commit()

        return redirect(url_for('products.products'))

    cur.execute("SELECT COUNT(*) FROM products WHERE name LIKE ?", ('%' + filter_query + '%',))
    total = cur.fetchone()[0]
    total_pages = (total + per_page - 1) // per_page

    return render_template('products.html',
                           products=products,
                           page=page,
                           total_pages=total_pages,
                           current_sort=sort_query,
                           filter_query=filter_query)

@products_blueprint.route('/edit_product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    db = get_db()
    cur = db.cursor()

    name = request.form['name']
    color = request.form['color']
    bud_type = request.form['bud_type']  # 꽃봉오리 타입 필드 추가
    cur.execute("UPDATE products SET name = ?, color = ?, bud_type = ? WHERE id = ?", (name, color, bud_type, product_id))
    db.commit()
    return "Success", 200