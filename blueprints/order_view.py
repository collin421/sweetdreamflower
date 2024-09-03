from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from .func import get_db

order_view_blueprint = Blueprint('order_view', __name__, template_folder='templates')

@order_view_blueprint.route('/order/confirmation/<int:order_id>')
def order_confirmation(order_id):
    db = get_db()
    cur = db.cursor()
    
    # 주문 정보 가져오기
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order_info = cur.fetchone()

    branch_name = 'Unknown'  # 기본값
    order_details = []       # 주문 세부사항을 위한 기본 빈 리스트

    if order_info:  # 주문 정보가 None이 아닌지 확인
        # 지점 정보 가져오기
        cur.execute("SELECT name FROM branches WHERE id = ?", (order_info['branch_id'],))
        branch_row = cur.fetchone()
        if branch_row:
            branch_name = branch_row['name']
        
        # 주문 세부사항 가져오기, 'order_details' 테이블이 있다고 가정
        cur.execute("SELECT product_name, color, quantity FROM order_details WHERE order_id = ?", (order_id,))
        order_details = cur.fetchall()

    cur.close()  # 작업 후 커서 닫기
    
    # 템플릿에 주문 정보, 지점 이름, 주문 세부사항 전달
    return render_template('order_confirmation.html', 
                           order=order_info, 
                           branch_name=branch_name, 
                           order_details=order_details)