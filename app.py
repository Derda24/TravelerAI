from flask import Flask, render_template, request
from supabase_client import supabase

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    query = None
    comparison = None

    if request.method == "POST":
        query = request.form.get("product", "").strip()
        if query:
            res = supabase.table("products")\
                .select("name, price, store_id, category")\
                .ilike("name", f"%{query}%")\
                .execute()
            items = res.data
            if not items:
                comparison = {"message": f"No matching products found for {query}."}
            else:
                comp = {}
                for item in items:
                    key = item["name"]
                    if key not in comp or item["price"] < comp[key]["price"]:
                        comp[key] = {"price": item["price"], "store": item["store_id"], "category": item["category"]}
                comparison = { k: [v] for k, v in comp.items() }
    else:
        # GET isteğinde tüm ürünleri listele
        res = supabase.table("products").select("name, price, store_id, category").execute()
        items = res.data or []
        comp = {}
        for item in items:
            key = item["name"]
            if key not in comp or item["price"] < comp[key]["price"]:
                comp[key] = {"price": item["price"], "store": item["store_id"], "category": item["category"]}
        comparison = { k: [v] for k, v in comp.items() }

    return render_template("index.html", query=query, comparison=comparison)

if __name__ == "__main__":
    app.run(debug=True)
