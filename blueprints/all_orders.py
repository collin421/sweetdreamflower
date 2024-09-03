from flask import Blueprint, request, render_template, send_file, jsonify
from collections import defaultdict
from io import BytesIO, StringIO
import pandas as pd
from .func import get_db

# 블루프린트 설정
all_orders_blueprint = Blueprint('all_orders', __name__, template_folder='templates')

@all_orders_blueprint.route('/all_orders', methods=['GET', 'POST'])
def all_orders():
    db = get_db()  # 데이터베이스 연결 가져오기
    selected_date = None  # 선택된 날짜 초기화
    orders_by_branch = defaultdict(list)  # 지점별 주문 초기화

    if request.method == 'POST':
        selected_date = request.form.get('order_date')  # 폼에서 선택된 날짜 가져오기
        cur = db.cursor()  # 커서 생성
        
        # 지점별 조회 쿼리 실행
        cur.execute('''
            SELECT b.name as branch_name, od.bud_type, od.product_name, od.color, SUM(od.quantity) as total_quantity, o.special_note
            FROM orders o
            JOIN branches b ON o.branch_id = b.id
            JOIN order_details od ON o.id = od.order_id
            WHERE o.order_date = ?
            GROUP BY b.name, od.bud_type, od.product_name, od.color, o.special_note
            ORDER BY od.bud_type, od.product_name, b.name
        ''', (selected_date,))
        
        # 조회 결과를 지점별로 정리
        for row in cur.fetchall():
            branch_name = row['branch_name']
            product_info = {
                'bud_type': row['bud_type'],
                'product_name': row['product_name'],
                'color': row['color'],
                'total_quantity': row['total_quantity'],
                'special_note': row['special_note']
            }
            orders_by_branch[branch_name].append(product_info)
        cur.close()  # 커서 닫기

    # 템플릿 렌더링
    return render_template('all_orders.html', orders_by_branch=orders_by_branch, selected_date=selected_date)


@all_orders_blueprint.route('/all_orders_by_bud_type', methods=['POST'])
def all_orders_by_bud_type():
    db = get_db()
    selected_date = request.form.get('order_date')
    orders_by_bud_type = defaultdict(lambda: defaultdict(list))
    product_totals = defaultdict(int)

    cur = db.cursor()
    
    cur.execute('''
        SELECT od.bud_type, od.product_name, SUM(od.quantity) as total_quantity, 
               b.name as branch_name, o.special_note
        FROM orders o
        JOIN order_details od ON o.id = od.order_id
        JOIN branches b ON o.branch_id = b.id
        WHERE o.order_date = ?
        GROUP BY od.bud_type, od.product_name, b.name, o.special_note
        ORDER BY od.bud_type, od.product_name, b.name
    ''', (selected_date,))
    
    for row in cur.fetchall():
        bud_type = row['bud_type']
        product_name = row['product_name']
        total_quantity = row['total_quantity']
        product_totals[(bud_type, product_name)] += total_quantity
        product_info = {
            'branch_name': row['branch_name'],
            'total_quantity': total_quantity,
            'special_note': row['special_note']
        }
        orders_by_bud_type[bud_type][product_name].append(product_info)
    cur.close()

    return render_template('all_orders.html', 
                           orders_by_bud_type=orders_by_bud_type, 
                           product_totals=product_totals, 
                           selected_date=selected_date)

@all_orders_blueprint.route('/download_all_orders', methods=['POST'])
def download_all_orders():
    selected_date = request.form.get('order_date')  # 폼에서 선택된 날짜 가져오기
    db = get_db()  # 데이터베이스 연결 가져오기
    cur = db.cursor()  # 커서 생성
    
    # 선택된 날짜의 모든 주문 데이터 조회
    cur.execute('''
        SELECT b.name as branch_name, od.bud_type, od.product_name, od.color, SUM(od.quantity) as total_quantity
        FROM orders o
        JOIN branches b ON o.branch_id = b.id
        JOIN order_details od ON o.id = od.order_id
        WHERE o.order_date = ?
        GROUP BY b.name, od.bud_type, od.product_name, od.color
        ORDER BY od.bud_type, od.product_name, b.name
    ''', (selected_date,))
    
    orders_by_branch = defaultdict(list)  # 지점별 주문 초기화
    # 조회 결과를 지점별로 정리
    for row in cur.fetchall():
        branch_name = row['branch_name']
        bud_type = row['bud_type']
        product_name = row['product_name']
        color = row['color']
        total_quantity = row['total_quantity']
        orders_by_branch[branch_name].append({
            'bud_type': bud_type,
            'product_name': product_name,
            'color': color,
            'total_quantity': total_quantity
        })
    cur.close()  # 커서 닫기
    
    # DataFrame 생성
    df_list = []
    for branch_name, orders in orders_by_branch.items():
        for order in orders:
            df_list.append({
                'Branch Name': branch_name,
                'Bud Type': order['bud_type'],
                'Product Name': order['product_name'],
                'Color': order['color'],
                'Total Quantity': order['total_quantity']
            })
    df = pd.DataFrame(df_list)
    
    # CSV 파일로 변환
    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Convert StringIO to BytesIO for binary mode
    response = BytesIO()
    response.write(output.getvalue().encode())
    response.seek(0)

    filename = f"all_orders_{selected_date}.csv"
    # CSV 파일 다운로드 응답 반환
    return send_file(response, as_attachment=True,
                     download_name=filename,
                     mimetype='text/csv')

@all_orders_blueprint.route('/download_all_orders_by_bud_type', methods=['POST'])
def download_all_orders_by_bud_type():
    selected_date = request.form.get('order_date')  # 폼에서 선택된 날짜 가져오기
    db = get_db()  # 데이터베이스 연결 가져오기
    cur = db.cursor()  # 커서 생성
    
    # 선택된 날짜의 모든 꽃봉오리 타입별 주문 데이터 조회
    cur.execute('''
        SELECT od.product_name, od.bud_type, SUM(od.quantity) as total_quantity, b.name as branch_name, o.special_note
        FROM orders o
        JOIN order_details od ON o.id = od.order_id
        JOIN branches b ON o.branch_id = b.id
        WHERE o.order_date = ?
        GROUP BY od.product_name, od.bud_type, b.name, o.special_note
        ORDER BY od.product_name, od.bud_type, b.name
    ''', (selected_date,))
    
    orders_by_bud_type = defaultdict(list)  # 꽃봉오리 타입별 주문 초기화
    product_totals = defaultdict(int)  # 꽃 이름별 합계 초기화

    # 조회 결과를 꽃봉오리 타입별로 정리 및 꽃 이름별 합계 계산
    for row in cur.fetchall():
        bud_type = row['bud_type']
        product_name = row['product_name']
        total_quantity = row['total_quantity']
        product_totals[product_name] += total_quantity
        product_info = {
            'product_name': product_name,
            'total_quantity': total_quantity,
            'branch_name': row['branch_name'],
            'special_note': row['special_note']
        }
        orders_by_bud_type[bud_type].append(product_info)
    cur.close()  # 커서 닫기

    # DataFrame 생성
    df_list = []
    for bud_type, orders in orders_by_bud_type.items():
        for order in orders:
            df_list.append({
                'Bud Type': bud_type,
                'Product Name': order['product_name'],
                'Total Quantity': order['total_quantity'],
                'Branch Name': order['branch_name'],
                'Special Note': order['special_note']
            })
    df = pd.DataFrame(df_list)
    
    # CSV 파일로 변환
    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Convert StringIO to BytesIO for binary mode
    response = BytesIO()
    response.write(output.getvalue().encode())
    response.seek(0)

    filename = f"all_orders_by_bud_type_{selected_date}.csv"
    # CSV 파일 다운로드 응답 반환
    return send_file(response, as_attachment=True,
                     download_name=filename,
                     mimetype='text/csv')
