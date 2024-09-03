from flask import Blueprint, request, render_template
from datetime import datetime, timedelta
import pandas as pd
import calendar
from .func import get_db

total_orders_blueprint = Blueprint('total_orders', __name__, template_folder='templates')

def week_range(year, week):
    # ISO 주 기준으로 해당 연도와 주차의 첫 번째 날짜 계산 (월요일 시작)
    firstday_of_week = datetime.strptime(f'{year}-W{int(week)}-1', "%Y-W%W-%w")
    # 첫 번째 날짜로부터 6일 후가 주의 마지막 날짜 (일요일)
    lastday_of_week = firstday_of_week + timedelta(days=6)
    return firstday_of_week.strftime("%Y-%m-%d"), lastday_of_week.strftime("%Y-%m-%d")


@total_orders_blueprint.route('/total_orders', methods=['GET', 'POST'])
def total_orders():
    db = get_db()
    today = datetime.today()

    # 기간별 차트 초기 설정 (최근 60일)
    default_end_date = today
    default_start_date = today - timedelta(days=59)  # 60일을 포함하기 위해 59일을 빼줌

    selected_start_date = request.form.get('start_date', default_start_date.strftime('%Y-%m-%d'))
    selected_end_date = request.form.get('end_date', default_end_date.strftime('%Y-%m-%d'))

    # 기간별 데이터 조회 SQL 쿼리
    period_sql_query = '''
        SELECT order_date, SUM(quantity) as total_quantity
        FROM orders
        JOIN order_details ON orders.id = order_details.order_id
        WHERE order_date BETWEEN ? AND ?
        GROUP BY order_date
    '''
    period_df = pd.read_sql(period_sql_query, db, params=(selected_start_date, selected_end_date))
    period_data = format_chart_data(period_df, pd.to_datetime(selected_start_date), pd.to_datetime(selected_end_date))

    # 초기 설정
    selected_year_week = today.year
    selected_week = today.isocalendar()[1]
    selected_year_month = today.year
    selected_month = today.month

    # 한글 요일 매핑
    day_name_korean = {
        'Monday': '월요일',
        'Tuesday': '화요일',
        'Wednesday': '수요일',
        'Thursday': '목요일',
        'Friday': '금요일',
        'Saturday': '토요일',
        'Sunday': '일요일'
    }

    if request.method == 'POST':
        if 'year_week' in request.form and 'week' in request.form:
            selected_year_week = int(request.form['year_week'])
            selected_week = int(request.form['week'])
            print(selected_year_week)
            print(selected_week)
        if 'year_month' in request.form and 'month' in request.form:
            selected_year_month = int(request.form['year_month'])
            selected_month = int(request.form['month'])
            print(selected_year_month)
            print(selected_month)

    # 주간 차트 데이터 계산
    year_start_week = datetime(selected_year_week, 1, 1)
    if year_start_week.weekday() != 6:
        year_start_week -= timedelta(days=year_start_week.weekday() + 1)
    weekly_start_date = year_start_week + timedelta(weeks=selected_week - 1)
    data_end_date_week = weekly_start_date + timedelta(days=7)

    display_start_date_week = weekly_start_date + timedelta(days=1)
    display_end_date_week = data_end_date_week
    print(display_end_date_week)
    print(display_start_date_week)

    # 월간 차트 데이터 계산
    monthly_start_date = datetime(selected_year_month, selected_month, 1)
    monthly_end_date = monthly_start_date + timedelta(days=calendar.monthrange(selected_year_month, selected_month)[1] - 1)
    print(monthly_start_date)
    print(monthly_end_date)

    # SQL 쿼리 및 데이터 처리
    sql_query = '''
        SELECT order_date, SUM(quantity) as total_quantity
        FROM orders
        JOIN order_details ON orders.id = order_details.order_id
        WHERE order_date BETWEEN ? AND ?
        GROUP BY order_date
    '''
    weekly_df = pd.read_sql(sql_query, db, params=(weekly_start_date, data_end_date_week))
    monthly_df = pd.read_sql(sql_query, db, params=(monthly_start_date, monthly_end_date))
    print(weekly_df)
    print(monthly_df)
    
    # 데이터 포맷팅 및 안전한 리스트 생성
    weekly_data = format_chart_data(weekly_df, display_start_date_week, display_end_date_week, day_name_korean)
    monthly_data = format_chart_data(monthly_df, monthly_start_date, monthly_end_date)
    print(weekly_data)
    print(monthly_data)

    years = range(2020, today.year + 1)
    months = range(1, 13)
    weeks = range(1, 53)
    
    weeks_display = {}
    for week in weeks:
        # week_range 함수를 호출하여 올바른 주차 범위를 가져옵니다.
        start_date, end_date = week_range(selected_year_week, week)
        weeks_display[week] = f'{week}주차 : {start_date}~{end_date}'

    return render_template('total_orders.html',
                           weeks_display=weeks_display,
                           weekly_data=weekly_data,
                           monthly_data=monthly_data,
                           years_week=years,
                           weeks=weeks,
                           years_month=years,
                           months=months,
                           selected_year_week=selected_year_week,
                           selected_week=selected_week,
                           selected_year_month=selected_year_month,
                           selected_month=selected_month,
                           period_data=period_data,
                           selected_start_date=selected_start_date,
                           selected_end_date=selected_end_date)

def format_chart_data(df, start_date, end_date, day_name_korean=None):
    # 날짜 범위 생성
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    # 데이터 초기화
    data = {
        'dates': [date.strftime('%Y-%m-%d') for date in date_range],
        'datedays': [date.strftime('%d') for date in date_range],
        'dayname': [day_name_korean[date.strftime('%A')] for date in date_range] if day_name_korean else [],
        'quantities': [0] * len(date_range)  # 모든 값 0으로 초기화
    }
    
    # 데이터프레임에서 날짜를 문자열로 변환 (필요한 경우)
    df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')

    # 날짜별로 수량 매핑
    for i, date in enumerate(data['dates']):
        match = df[df['order_date'] == date]
        if not match.empty:
            data['quantities'][i] = int(match['total_quantity'].iloc[0])

    return data