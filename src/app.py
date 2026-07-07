"""
app.py — Flipkart Product Price & Deal Analytics Dashboard
Run: streamlit run src/app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(__file__))
from price_analysis import analyze

st.set_page_config(page_title="Flipkart Price Analytics", page_icon="🛒", layout="wide")

@st.cache_data
def load():
    df, cat_summary, brand_summary = analyze()
    df["listing_date"] = pd.to_datetime(df["listing_date"])
    return df, cat_summary, brand_summary

df, cat_summary, brand_summary = load()

st.title("🛒 Flipkart Product Price & Deal Analytics")
st.caption("Pricing strategy, discount trends, and deal-quality scoring across 5,000+ product listings")

category_filter = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
filtered = df[df["category"].isin(category_filter)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Products", f"{len(filtered):,}")
c2.metric("Avg Discount", f"{filtered['discount_pct'].mean():.1f}%")
c3.metric("Avg Selling Price", f"₹{filtered['selling_price'].mean():,.0f}")
c4.metric("Avg Deal Score", f"{filtered['deal_score'].mean():.1f}/100")

col1, col2 = st.columns(2)
with col1:
    disc_by_cat = filtered.groupby("category")["discount_pct"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(disc_by_cat, x="category", y="discount_pct", title="Average Discount % by Category",
                 color="discount_pct", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    price_trend = filtered.groupby(filtered["listing_date"].dt.to_period("M"))["selling_price"].mean().reset_index()
    price_trend["listing_date"] = price_trend["listing_date"].astype(str)
    fig2 = px.line(price_trend, x="listing_date", y="selling_price", markers=True,
                   title="Avg Selling Price Trend Over Time")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig3 = px.scatter(filtered.sample(min(1000, len(filtered))), x="discount_pct", y="rating",
                       color="category", title="Discount % vs Rating", opacity=0.6)
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    top_brands = brand_summary.head(10).reset_index()
    fig4 = px.bar(top_brands, x="avg_deal_score", y="brand", orientation="h",
                  title="Top 10 Brands by Deal Score")
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("🏆 Best Deals Right Now (Top Deal Score)")
best_deals = filtered.sort_values("deal_score", ascending=False).head(10)
st.dataframe(
    best_deals[["product_id", "category", "brand", "mrp", "selling_price", "discount_pct", "rating", "deal_score"]],
    use_container_width=True
)

st.subheader("Category Pricing Summary")
st.dataframe(cat_summary, use_container_width=True)

st.caption("Built with Python, Pandas, Streamlit, Plotly | Deal Score = weighted composite of discount, rating, popularity | Synthetic dataset modeled on real e-commerce pricing patterns")
