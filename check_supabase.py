#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bonnie_project.settings')
django.setup()

from django.db import connection
from django.conf import settings

def test_connection():
    db_config = settings.DATABASES['default']
    engine = db_config.get('ENGINE', '')
    host = db_config.get('HOST', 'local')
    name = db_config.get('NAME', '')

    print("=" * 60)
    print("BonnieInfratech - Database Connection Check")
    print("=" * 60)
    print(f"Engine: {engine}")
    print(f"Host:   {host}")
    print(f"Name:   {name}")

    if 'sqlite3' in engine:
        print("\nℹ️ Currently running on local SQLite database.")
        print("To switch to Supabase PostgreSQL, add your DATABASE_URL in the .env file:")
        print("  DATABASE_URL=postgresql://postgres.szsqfrijdlrlemczxzjj:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require\n")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print("\n🎉 Connection SUCCESSFUL! Connected to PostgreSQL.")
            print(f"Version: {version}\n")
    except Exception as e:
        print(f"\n❌ Connection FAILED: {e}\n")

if __name__ == '__main__':
    test_connection()
