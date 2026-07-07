"""
price_analysis.py — computes a rule-based "Deal Score" per product
(a common real-world analyst technique: composite scoring, not ML)
and category/brand-level pricing statistics.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def analyze():
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_PATH = BASE_DIR / "data" / "flipkart_products.csv"
    OUTPUT_PATH = BASE_DIR / "data" / "flipkart_products_scored.csv"

    df = pd.read_csv(DATA_PATH)

    # Normalize each factor to 0-1 within its category for fair comparison
    def normalize(s):
        return (s - s.min()) / (s.max() - s.min() + 1e-9)

    df["discount_norm"] = df.groupby("category")["discount_pct"].transform(normalize)
    df["rating_norm"] = df.groupby("category")["rating"].transform(normalize)
    df["popularity_norm"] = df.groupby("category")["num_ratings"].transform(normalize)

    # Composite Deal Score
    df["deal_score"] = (
        0.5 * df["discount_norm"]
        + 0.35 * df["rating_norm"]
        + 0.15 * df["popularity_norm"]
    ).round(3) * 100

    df.to_csv(OUTPUT_PATH, index=False)

    category_summary = (
        df.groupby("category")
        .agg(
            avg_mrp=("mrp", "mean"),
            avg_selling_price=("selling_price", "mean"),
            avg_discount_pct=("discount_pct", "mean"),
            avg_rating=("rating", "mean"),
            products=("product_id", "count"),
        )
        .round(2)
        .sort_values("avg_discount_pct", ascending=False)
    )

    brand_summary = (
        df.groupby("brand")
        .agg(
            avg_discount_pct=("discount_pct", "mean"),
            avg_deal_score=("deal_score", "mean"),
            products=("product_id", "count"),
        )
        .round(2)
        .sort_values("avg_deal_score", ascending=False)
    )

    return df, category_summary, brand_summary


if __name__ == "__main__":
    analyze()