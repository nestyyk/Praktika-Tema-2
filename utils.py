from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def print_header(text):
    print("\n" + "="*60)
    print(f"{' ' * 20}{text}")
    print("="*60)