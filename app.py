from flask import Flask, render_template, request
from supabase import create_client, Client
from scraper import compare_products  # your compare function

# Supabase setup
SUPABASE_URL = "https://behwybmvebhrggxxkyqs.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlaHd5Ym12ZWJocmdneHhreXFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQwMjAwODYsImV4cCI6MjA1OTU5NjA4Nn0.ChkEGsaJaXidGKSkiTQ6msN0xuUS81zhzoex32gwjQ4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

app = Flask(__name__)

@app.route('/compare', methods=['GET','POST'])
def compare():
    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        category     = request.form.get('category')
        comparison = compare_products(product_name, category)
        return render_template("comparison.html",
                               product_name=product_name,
                               category=category,
                               comparison=comparison)
    else:
        # If someone does GET /compare, just redirect back to home
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
