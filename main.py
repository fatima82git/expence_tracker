import sqlite3
from datetime import datetime

# اتصال به دیتابیس
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# ساخت جدول
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        category TEXT,
        amount REAL,
        description TEXT,
        date TEXT
    )
''')
conn.commit()

def add_transaction(type, category, amount, description):
    date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        INSERT INTO transactions (type, category, amount, description, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (type, category, amount, description, date))
    conn.commit()
    print(f"✅ ثبت شد: {type} | {category} | {amount}")

def monthly_report():
    month = datetime.now().strftime('%Y-%m')
    cursor.execute('''
        SELECT type, SUM(amount) FROM transactions
        WHERE date LIKE ? GROUP BY type
    ''', (f'{month}%',))
    results = cursor.fetchall()
    print(f"\n📊 گزارش {month}:")
    for row in results:
        print(f"  {row[0]}: {row[1]:,.0f} تومان")

def show_all():
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = cursor.fetchall()
    print("\n📋 همه تراکنش‌ها:")
    for row in rows:
        print(f"  {row[5]} | {row[1]} | {row[2]} | {row[4]} | {row[3]:,.0f}")

def menu():
    while True:
        print("\n=== مدیریت هزینه ===")
        print("1. ثبت درآمد")
        print("2. ثبت خرج")
        print("3. گزارش ماهانه")
        print("4. نمایش همه")
        print("5. خروج")
        choice = input("انتخاب: ")

        if choice == '1':
            cat = input("دسته‌بندی (حقوق/فریلنس/دیگر): ")
            amt = float(input("مبلغ: "))
            desc = input("توضیح: ")
            add_transaction('income', cat, amt, desc)
        elif choice == '2':
            cat = input("دسته‌بندی (غذا/حمل‌ونقل/قبوض/دیگر): ")
            amt = float(input("مبلغ: "))
            desc = input("توضیح: ")
            add_transaction('expense', cat, amt, desc)
        elif choice == '3':
            monthly_report()
        elif choice == '4':
            show_all()
        elif choice == '5':
            print("خروج...")
            break

if __name__ == '__main__':
    menu()
