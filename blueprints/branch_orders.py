from flask import Blueprint, request, render_template, jsonify
from .func import get_db  # func 모듈에서 get_db 함수를 가져옵니다.

branch_orders_blueprint = Blueprint('branch_orders', __name__, template_folder='templates')

@branch_orders_blueprint.route('/branch_orders', methods=['GET', 'POST'])
def branch_orders():
    db = get_db()
    branches = db.execute('SELECT id, name FROM branches').fetchall()
    branches_dict = {branch['id']: branch['name'] for branch in branches}  # 지점 ID와 이름 매핑

    selected_date = request.form.get('order_date') if request.method == 'POST' else None
    selected_branch_id = request.form.get('branch_id')
    orders = []

    if selected_date:
        if selected_branch_id == 'all':
            orders = db.execute('''
                SELECT o.id, o.order_date, od.product_name, od.color, od.quantity, o.branch_id
                FROM orders o
                JOIN order_details od ON o.id = od.order_id
                WHERE o.order_date = ?
            ''', (selected_date,)).fetchall()
        elif selected_branch_id:
            orders = db.execute('''
                SELECT o.id, o.order_date, od.product_name, od.color, od.quantity, o.branch_id
                FROM orders o
                JOIN order_details od ON o.id = od.order_id
                WHERE o.order_date = ? AND o.branch_id = ?
            ''', (selected_date, int(selected_branch_id))).fetchall()

    return render_template('branch_orders.html', branches=branches, branches_dict=branches_dict, orders=orders, selected_date=selected_date, selected_branch_id=selected_branch_id)

@branch_orders_blueprint.route('/update_order', methods=['POST'])
def update_order():
    # 데이터베이스 연결
    db = get_db()

    # JSON 데이터 파싱
    data = request.get_json()  # 이 부분이 변경되었습니다.
    order_id = data['order_id']
    product_name = data['product_name']
    color = data['color']
    quantity = data['quantity']

    # 데이터베이스 업데이트 쿼리 실행
    db.execute('''
        UPDATE order_details
        SET product_name = ?, color = ?, quantity = ?
        WHERE id = ?
    ''', (product_name, color, quantity, order_id))
    db.commit()

    # 성공적으로 업데이트되었음을 클라이언트에 알림
    return jsonify({'status': 'success'})

@branch_orders_blueprint.route('/delete_order', methods=['POST'])
def delete_order():
    db = get_db()
    order_id = request.get_json()['order_id']

    db.execute('DELETE FROM order_details WHERE id = ?', (order_id,))
    db.commit()

    return jsonify({'status': 'success'})
