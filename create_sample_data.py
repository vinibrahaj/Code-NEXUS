import os

DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "messy.csv")

CSV_CONTENT = """id,name,age,email
1,  Alice   , 23  , alice@example.com
2,BOB,  ,bob@example.com
3,   charlie,17,charlie@example.com
3,   charlie,17,charlie@example.com
4,,29,no_name@example.com
5, Diana  , -2 , diana@example.com
6,Ed,not_a_number, ed@example.com
7,   Fay , 42, fay@example.com
"""

def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(CSV_CONTENT)

    print(f"Sample data created at: {FILE_PATH}")

if __name__ == "__main__":
    main()
