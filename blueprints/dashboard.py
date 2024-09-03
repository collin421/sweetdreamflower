from flask import Blueprint, render_template, request, send_file
from .func import get_db
import datetime
import pandas as pd
from io import BytesIO

# Blueprint 객체 생성
dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='templates')

# 대시보드 라우트 정의
@dashboard_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # 데이터베이스 연결 객체 가져오기
    db = get_db()
    
    # 현재 연도를 가져오고 선택된 연도를 폼 데이터에서 가져오기 (기본값: 현재 연도)
    current_year = datetime.datetime.now().year
    selected_year = int(request.form.get('year', current_year))
    
    # 모든 지점 이름 가져오기
    cur = db.cursor()
    cur.execute('SELECT DISTINCT name FROM branches')
    branches = [row['name'] for row in cur.fetchall()]
    
    # 선택된 연도의 시작 및 종료 날짜 계산
    start_date = datetime.date(selected_year, 1, 1)
    end_date = datetime.date(selected_year, 12, 31)
    dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    # 선택된 연도의 매출 데이터 가져오기
    cur.execute('''
        SELECT s.sale_date, b.name AS branch_name, 
               s.sales_card_sweetdream, s.sales_card_glory, 
               s.sales_cash, s.sales_zeropay, 
               s.sales_transfer, s.total_sales
        FROM sales s
        JOIN branches b ON s.branch_id = b.id
        WHERE strftime('%Y', s.sale_date) = ?
        ORDER BY s.sale_date, b.name
    ''', (str(selected_year),))
    
    # 쿼리 결과를 변수에 저장
    sales_data = cur.fetchall()
    cur.close()
    
    # 매출 데이터를 지점별로 초기화
    sales_by_branch = {branch: {date: {'sales_card_sweetdream': 0, 'sales_card_glory': 0, 'sales_cash': 0, 'sales_zeropay': 0, 'sales_transfer': 0, 'total_sales': 0} for date in dates} for branch in branches}
    total_sales_by_date = {date: 0 for date in dates}
    
    # 쿼리 결과를 통해 매출 데이터를 계산
    for row in sales_data:
        date = datetime.datetime.strptime(row['sale_date'], '%Y-%m-%d').date()
        branch = row['branch_name']
        sales_by_branch[branch][date]['sales_card_sweetdream'] += row['sales_card_sweetdream']
        sales_by_branch[branch][date]['sales_card_glory'] += row['sales_card_glory']
        sales_by_branch[branch][date]['sales_cash'] += row['sales_cash']
        sales_by_branch[branch][date]['sales_zeropay'] += row['sales_zeropay']
        sales_by_branch[branch][date]['sales_transfer'] += row['sales_transfer']
        sales_by_branch[branch][date]['total_sales'] += row['total_sales']
        total_sales_by_date[date] += row['total_sales']
    
    # 템플릿에 데이터를 전달하여 렌더링
    return render_template('dashboard.html', 
                           sales_by_branch=sales_by_branch, 
                           dates=dates, 
                           branches=branches, 
                           selected_year=selected_year, 
                           current_year=current_year, 
                           total_sales_by_date=total_sales_by_date,
                           today=datetime.date.today())

# CSV 다운로드 라우트 정의
@dashboard_blueprint.route('/download-sales-csv')
def download_sales_csv():
    try:
        # 데이터베이스 연결 객체 가져오기
        db = get_db()
        cur = db.cursor()
        
        # 현재 연도를 기본값으로 설정
        selected_year = datetime.datetime.now().year
        start_date = datetime.date(selected_year, 1, 1)
        end_date = datetime.date(selected_year, 12, 31)
        date_range = pd.date_range(start=start_date, end=end_date)

        # 선택된 연도의 매출 데이터 가져오기
        cur.execute('''
            SELECT s.sale_date, b.name AS branch_name, s.sales_card_sweetdream, s.sales_card_glory, 
                   s.sales_cash, s.sales_zeropay, s.sales_transfer, s.total_sales
            FROM sales s
            JOIN branches b ON s.branch_id = b.id
            WHERE strftime('%Y', s.sale_date) = ?
            ORDER BY s.sale_date, b.name
        ''', (str(selected_year),))
        sales_data = cur.fetchall()
        cur.close()

        # 쿼리 결과를 데이터프레임으로 변환
        sales_df = pd.DataFrame(sales_data, columns=['sale_date', 'branch_name', 'sales_card_sweetdream', 'sales_card_glory', 'sales_cash', 'sales_zeropay', 'sales_transfer', 'total_sales'])
        sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])

        # 모든 날짜에 대한 데이터프레임 생성
        all_dates_df = pd.DataFrame(date_range, columns=['sale_date'])

        # 병합을 위한 'sale_date' 열을 datetime 형식으로 변환
        merged_df = pd.merge(all_dates_df, sales_df, on='sale_date', how='left').fillna(0)

        # 디버깅: 데이터프레임 내용 출력
        print(merged_df.head())

        # 데이터프레임을 CSV 파일로 변환
        output = BytesIO()
        merged_df.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)

        # CSV 파일을 클라이언트에게 전송
        return send_file(output, download_name=f"sales_data_{selected_year}.csv", as_attachment=True, mimetype='text/csv')
    
    except Exception as e:
        # 오류 발생 시, 오류 메시지를 출력
        print(f"Error: {e}")
        return "CSV 파일을 생성하는 동안 오류가 발생했습니다.", 500

