import sqlite3
import pytest
from playwright.sync_api import expect

def test_database_integrity(page):
    # 1. Navigate to the app
    page.goto("http://127.0.0.1:5000")
    
    # 2. LOGIN (With a wait to prevent timeouts)
    page.wait_for_selector("#username", state="visible", timeout=5000)
    page.locator("#username").fill("qa_user")
    page.locator("#password").fill("password123")
    page.locator("#login-btn").click()
    
    # 3. PERFORM TRANSFER (Wait for Dashboard to load)
    page.wait_for_selector("#amount", state="visible", timeout=5000)
    unique_amount = 900.0  # Changed to float to match DB type
    page.locator("#amount").fill(str(int(unique_amount))) # Fill UI with '900'
    page.select_option("#currency", "EUR")
    page.locator("#transfer-btn").click()
    
    # 4. SYNCHRONIZATION POINT (CRITICAL)
    # Wait for the UI success message BEFORE we check the database.
    # This ensures Flask has finished writing to the SQLite file.
    success_message = page.locator("#success-msg")
    expect(success_message).to_be_visible(timeout=10000)
    
   # 5. DATABASE CHECK
    conn = sqlite3.connect("instance/app.db")
    cursor = conn.cursor()
    
    # FIX: We put "transaction" in quotes because it's a reserved SQL word.
    # FIX: We use a parameterized query (?) which is best practice for SQL!
    query = 'SELECT amount_usd, target_currency FROM "transaction" WHERE amount_usd=? ORDER BY id DESC LIMIT 1'
    cursor.execute(query, (unique_amount,))
    
    row = cursor.fetchone()
    conn.close()
    
# 6. ASSERTIONS
    assert row is not None, "Transaction not found in Database!"
    # Now comparing 900.0 == 900.0
    assert row[0] == unique_amount, f"Expected {unique_amount} in DB but found {row[0]}"
    assert row[1] == "EUR", f"Expected EUR in DB but found {row[1]}"
    
    print(f"\n✅ Data Integrity Verified: {row[0]} matches {unique_amount} perfectly!")