#!/usr/bin/env python3
"""
在命令行展示数据库数据的脚本（简化版，不需要额外依赖）
用法:
    python show_db_simple.py                    # 展示所有表数据
    python show_db_simple.py --table worlds     # 只展示指定表
    python show_db_simple.py --list             # 列出所有表名
"""

import sqlite3
import json
import argparse
import sys
import io

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_FILE = "mini_api.db"


def get_table_names(conn):
    """获取所有表名"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    tables.sort()
    return tables


def format_json(data):
    """格式化 JSON 数据"""
    if data is None:
        return "NULL"
    try:
        parsed = json.loads(data) if isinstance(data, str) else data
        return json.dumps(parsed, ensure_ascii=False)
    except:
        return str(data)


def safe_str(s):
    """安全的字符串转换，处理编码问题"""
    if s is None:
        return "NULL"
    s = str(s)
    # 替换可能导致编码问题的字符
    return s.encode('gbk', errors='replace').decode('gbk')


def show_table(conn, table_name, limit=None):
    """展示指定表的数据"""
    cursor = conn.cursor()

    # 获取列信息
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]

    # 获取数据
    query = f"SELECT * FROM {table_name}"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print(f"\n表 '{table_name}' 没有数据\n")
        return

    print(f"\n{'='*80}")
    print(f"表: {table_name} (共 {len(rows)} 条记录)")
    print(f"{'='*80}")

    for row_idx, row in enumerate(rows):
        print(f"\n--- 记录 {row_idx + 1} ---")
        for col_name, val in zip(column_names, row):
            if isinstance(val, str) and (val.startswith('[') or val.startswith('{')):
                val = format_json(val)
            print(f"{col_name:20s}: {safe_str(val)}")


def show_all_tables(conn):
    """展示所有表"""
    tables = get_table_names(conn)
    for table in tables:
        show_table(conn, table)


def list_tables(conn):
    """列出所有表名"""
    tables = get_table_names(conn)
    print(f"\n数据库中的表 (共 {len(tables)} 个):")
    print("-" * 40)
    for i, table in enumerate(tables, 1):
        # 获取记录数
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{i:2d}. {table:20s} ({count} 条记录)")
    print()


def main():
    parser = argparse.ArgumentParser(description="在命令行展示数据库数据")
    parser.add_argument("--table", "-t", help="只展示指定表")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有表名")
    parser.add_argument("--limit", type=int, default=None, help="限制展示的记录数")

    args = parser.parse_args()

    conn = sqlite3.connect(DB_FILE)

    try:
        if args.list:
            list_tables(conn)
        elif args.table:
            show_table(conn, args.table, args.limit)
        else:
            show_all_tables(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
