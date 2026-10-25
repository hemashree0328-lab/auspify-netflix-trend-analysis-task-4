
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Set up folders
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 2. Load the dataset
df = pd.read_csv(BASE_DIR / "Dataset.csv")
df.columns = df.columns.str.strip()

print("=" * 55)
print("AUSPIFY TASK 4: NETFLIX RELEASE YEAR TREND ANALYSIS")
print("=" * 55)
print("Dataset loaded:", df.shape)

# 3. Remove duplicate records
df = df.drop_duplicates()

# 4. Clean release year
df["release_year"] = pd.to_numeric(
    df["release_year"], errors="coerce"
)

df = df.dropna(subset=["release_year"]).copy()
df["release_year"] = df["release_year"].astype(int)

# Keep plausible release years
df = df[
    df["release_year"].between(1900, 2026)
].copy()

# 5. Calculate yearly content releases
yearly = (
    df.groupby("release_year")
    .size()
    .reset_index(name="content_count")
    .sort_values("release_year")
)

yearly.to_csv(
    OUTPUT_DIR / "yearly_content_trends.csv",
    index=False
)

# 6. Calculate yearly releases by content type
type_yearly = (
    df.groupby(["release_year", "type"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

type_yearly.to_csv(
    OUTPUT_DIR / "yearly_content_by_type.csv"
)

# 7. Calculate year-over-year changes
yearly["yearly_change"] = yearly["content_count"].diff()

yearly["growth_percentage"] = (
    yearly["content_count"]
    .pct_change()
    .mul(100)
    .round(2)
)

yearly.to_csv(
    OUTPUT_DIR / "yearly_content_trends.csv",
    index=False
)

# 8. Create yearly trend chart
plt.figure(figsize=(12, 6))
plt.plot(
    yearly["release_year"],
    yearly["content_count"],
    marker="o"
)
plt.title("Netflix Titles by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "yearly_release_trend.png",
    dpi=300
)
plt.close()

# 9. Create Movie vs TV Show trend chart
type_yearly.plot(figsize=(12, 6))
plt.title("Netflix Movies and TV Shows by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "content_type_trends.png",
    dpi=300
)
plt.close()

# 10. Identify peak year and summarize findings
peak = yearly.loc[yearly["content_count"].idxmax()]

latest_year = yearly["release_year"].max()
latest_count = yearly.loc[
    yearly["release_year"] == latest_year,
    "content_count"
].iloc[0]

with open(
    OUTPUT_DIR / "business_insights.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("AUSPIFY TASK 4: BUSINESS INSIGHTS\n\n")
    file.write(
        f"Peak release year in the dataset: "
        f"{peak['release_year']}\n"
    )
    file.write(
        f"Titles in peak year: {peak['content_count']}\n"
    )
    file.write(
        f"Latest release year represented: {latest_year}\n"
    )
    file.write(
        f"Titles in latest year: {latest_count}\n\n"
    )
    file.write(
        "The analysis counts titles by their release year.\n"
    )
    file.write(
        "The charts compare yearly content patterns and "
        "Movie versus TV Show releases.\n\n"
    )
    file.write(
        "Note: Release year is not the same as the date "
        "Netflix added a title to its platform.\n"
    )
    file.write(
        "Recent years may be incomplete in the dataset, "
        "so interpret apparent declines cautiously.\n"
    )

# 11. Display results
print("\nTOP 10 YEARS BY NUMBER OF TITLES")
print(
    yearly.sort_values(
        "content_count", ascending=False
    ).head(10).to_string(index=False)
)

print("\nAnalysis completed successfully!")
print("Output folder:", OUTPUT_DIR.resolve())

for item in sorted(OUTPUT_DIR.iterdir()):
    print("-", item.name)
