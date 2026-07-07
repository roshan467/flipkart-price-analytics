"""
generate_data.py — synthetic e-commerce product pricing dataset modeled on
Flipkart's public listing structure (category, brand, MRP, selling price,
discount, rating) — generated programmatically for full reproducibility.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(21)
N = 5000

CATEGORIES = ["Smartphones", "Laptops", "Headphones", "Smartwatches",
              "Televisions", "Home Appliances", "Footwear", "Fashion"]
BRANDS = {
    "Smartphones": ["Samsung", "Xiaomi", "Realme", "Apple", "OnePlus", "Vivo"],
    "Laptops": ["HP", "Dell", "Lenovo", "Asus", "Acer", "Apple"],
    "Headphones": ["boAt", "JBL", "Sony", "Noise", "Boult"],
    "Smartwatches": ["Noise", "boAt", "Fire-Boltt", "Apple", "Samsung"],
    "Televisions": ["Samsung", "LG", "Mi", "Sony", "TCL"],
    "Home Appliances": ["LG", "Samsung", "Whirlpool", "Bosch", "Havells"],
    "Footwear": ["Puma", "Nike", "Adidas", "Bata", "Campus"],
    "Fashion": ["Levis", "Allen Solly", "H&M", "Roadster", "Van Heusen"],
}

def generate():
    rows = []
    start_date = datetime(2025, 1, 1)
    for i in range(N):
        category = np.random.choice(CATEGORIES)
        brand = np.random.choice(BRANDS[category])
        base_price = {
            "Smartphones": 15000, "Laptops": 45000, "Headphones": 2000,
            "Smartwatches": 3000, "Televisions": 30000, "Home Appliances": 12000,
            "Footwear": 1800, "Fashion": 1200,
        }[category]
        mrp = round(np.clip(np.random.gamma(2, base_price / 2), base_price * 0.5, base_price * 4) / 10) * 10

        # Premium brands discount less
        premium = brand in ["Apple", "Sony", "Nike", "Bosch"]
        discount_pct = np.random.normal(18 if premium else 32, 8)
        discount_pct = np.clip(discount_pct, 0, 70)
        selling_price = round(mrp * (1 - discount_pct / 100) / 10) * 10

        rating = np.clip(np.random.normal(4.0, 0.5), 1.5, 5.0).round(1)
        num_ratings = int(np.clip(np.random.exponential(800), 5, 50000))
        date = start_date + timedelta(days=int(np.random.uniform(0, 540)))

        rows.append({
            "product_id": f"FLP-{30000+i}",
            "category": category,
            "brand": brand,
            "mrp": mrp,
            "selling_price": selling_price,
            "discount_pct": round(discount_pct, 1),
            "rating": rating,
            "num_ratings": num_ratings,
            "listing_date": date.strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate()
    df.to_csv("/home/claude/FlipkartPriceAnalytics/data/flipkart_products.csv", index=False)
    print(f"Generated {len(df)} products across {df['category'].nunique()} categories")
    print(df.head())
