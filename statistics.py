from database import get_connection
from datetime import datetime

def get_order_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    # Общее количество заказов
    cursor.execute("SELECT COUNT(*) as count, SUM(total_amount) as sum FROM orders")
    total = cursor.fetchone()
    stats['total_orders'] = total['count']
    stats['total_revenue'] = round(total['sum'] or 0, 2)

    # Заказы по статусам
    cursor.execute("""
        SELECT status, COUNT(*) as count, SUM(total_amount) as sum 
        FROM orders GROUP BY status
    """)
    stats['by_status'] = {row['status']: {'count': row['count'], 'sum': round(row['sum'] or 0, 2)}
                         for row in cursor.fetchall()}

    # Топ-5 клиентов по сумме заказов
    cursor.execute('''
        SELECT c.full_name, COUNT(o.id) as orders_count, 
               SUM(o.total_amount) as total_sum
        FROM clients c
        JOIN orders o ON c.id = o.client_id
        GROUP BY c.id
        ORDER BY total_sum DESC LIMIT 5
    ''')
    stats['top_clients'] = cursor.fetchall()

    # Динамика заказов по месяцам (последние 6 месяцев)
    cursor.execute('''
        SELECT strftime('%Y-%m', order_date) as month, 
               COUNT(*) as count, SUM(total_amount) as sum
        FROM orders 
        WHERE order_date >= date('now', '-6 months')
        GROUP BY month
        ORDER BY month
    ''')
    stats['monthly'] = cursor.fetchall()

    conn.close()
    return stats