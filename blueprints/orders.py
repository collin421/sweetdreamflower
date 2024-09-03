from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from .func import get_db, generate_code

order_blueprint = Blueprint('order', __name__, template_folder='templates')

@order_blueprint.route('/order', methods=['GET', 'POST'])
def order():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        order_date = request.form.get('order_date')  # 날짜 정보 수집
        branch_id = request.form.get('branch_id')
        special_note = request.form.get('special_note')
        product_ids = request.form.getlist('product_id[]')
        colors = request.form.getlist('color[]')
        quantities = request.form.getlist('quantity[]')
        bud_types = request.form.getlist('bud_type[]')

        # 주문 정보를 데이터베이스에 저장
        order_code = generate_code(8)  # 주문 코드 생성
        cur.execute("INSERT INTO orders (order_date, branch_id, special_note, order_code) VALUES (?, ?, ?, ?)",
                    (order_date, branch_id, special_note, order_code))
        order_id = cur.lastrowid

        # 상세 주문 정보 저장
        for product_id_name, color, quantity, bud_type in zip(product_ids, colors, quantities, bud_types):
            product_id, product_name = product_id_name.split('|', 1)  # 품목 ID와 이름 분리
            cur.execute("INSERT INTO order_details (order_id, product_id, quantity, color, product_name, bud_type) VALUES (?, ?, ?, ?, ?, ?)",
                        (order_id, product_id, quantity, color, product_name, bud_type))
        db.commit()

        return redirect(url_for('order_view.order_confirmation', order_id=order_id))
    else:
        # 페이지 로딩 시 필요한 정보 로드
        return render_template('order.html')

@order_blueprint.route('/api/branches')
def api_branches():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, name, email FROM branches')
    branches = cur.fetchall()
    branches_list = [{'id': row['id'], 'name': row['name'], 'email': row['email']} for row in branches]
    cur.close()
    return jsonify(branches_list)

@order_blueprint.route('/api/products')
def api_products():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT DISTINCT name FROM products')
    products = cur.fetchall()
    products_list = [{'name': row['name']} for row in products]
    cur.close()
    return jsonify(products_list)

@order_blueprint.route('/api/colors/<product_name>')
def api_colors(product_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT DISTINCT color FROM products WHERE name = ?", (product_name,))
    colors = cur.fetchall()
    cur.close()
    return jsonify([row['color'] for row in colors])

@order_blueprint.route('/api/bud_types/<product_name>')
def api_bud_types(product_name):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT DISTINCT bud_type FROM products WHERE name = ?", (product_name,))
    bud_types = cur.fetchall()
    cur.close()
    return jsonify([row['bud_type'] for row in bud_types])
