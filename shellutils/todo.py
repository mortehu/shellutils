import argparse
import sys
import os
import sqlite3
from datetime import datetime

def find_project_directory():
    current_dir = os.path.abspath(os.getcwd())
    while current_dir != os.path.dirname(current_dir):
        if os.path.isdir(os.path.join(current_dir, ".git")):
            if os.stat(os.path.join(current_dir, ".git")).st_uid == os.getuid():
                return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

def get_database_path():
    project_dir = find_project_directory()
    if project_dir:
        return os.path.join(project_dir, ".todo.db")
    return os.path.expanduser("~/.local/share/todo.db")

def initialize_database(database_path):
    conn = sqlite3.connect(database_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS todos
                    (id INTEGER PRIMARY KEY, todo TEXT, created_at TIMESTAMP, done BOOLEAN)''')
    return conn

def print_todos(conn):
    for row in conn.execute("SELECT * FROM todos WHERE done = 0 ORDER BY created_at ASC"):
        print(f"{row[2]}: {row[1]}")

def add_todo(conn, todo):
    conn.execute("INSERT INTO todos (todo, created_at, done) VALUES (?, ?, 0)", (todo, datetime.now()))
    conn.commit()

def mark_done(conn, todo):
    conn.execute("UPDATE todos SET done = 1 WHERE todo = ? AND done = 0", (todo,))
    conn.commit()

def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple command line todo app.")
    parser.add_argument("todo", nargs="*", help="The todo to be added or marked as done.")
    parser.add_argument("--done", action="store_true", help="Mark a todo as done.")
    return parser.parse_args()

def main():
    args = parse_arguments()

    database_path = get_database_path()
    conn = initialize_database(database_path)
    
    if args.done:
        if args.todo:
            mark_done(conn, " ".join(args.todo))
        else:
            print("Usage: todo.py --done \"TODO text\"")
    elif args.todo:
        add_todo(conn, " ".join(args.todo))
    else:
        print_todos(conn)

    conn.close()

if __name__ == "__main__":
    main()
