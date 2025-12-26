import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.scrapethissite.com/pages/simple/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_countries():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("Страница не найдена")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    countries = []

    blocks = soup.find_all("div", class_="country")
    if not blocks:
        print("Данные не найдены")
        return []

    for block in blocks:
        def safe_text(parent, tag, class_name):
            el = parent.find(tag, class_=class_name)
            return el.get_text(strip=True) if el else ""

        name = safe_text(block, "h3", "country-name")
        capital = safe_text(block, "span", "country-capital")
        population = safe_text(block, "span", "country-population")
        area = safe_text(block, "span", "country-area")
        region = safe_text(block, "span", "country-region")

        if not name:
            continue

        countries.append({
            "country": name,
            "capital": capital,
            "population": int(population) if population.isdigit() else None,
            "area": float(area) if area else None,
            "region": region
        })

    return countries


def main():
    data = scrape_countries()
    print(f"\nСобрано стран: {len(data)}")

    if not data:
        print("Нет данных для анализа")
        return

    df = pd.DataFrame(data)

    df.to_csv("countries_dataset.csv", index=False, encoding="utf-8")
    print("CSV сохранён: countries_dataset.csv")

    print("\n=== INFO ===")
    print(df.info())

    print("\n=== DESCRIBE ===")
    print(df.describe())

    print("\n=== ТОП-5 СТРАН ПО НАСЕЛЕНИЮ ===")
    print(df.sort_values("population", ascending=False).head(5)[
        ["country", "population"]
    ])

    print("\n=== КОЛИЧЕСТВО СТРАН ПО РЕГИОНАМ ===")
    print(df["region"].value_counts())


if __name__ == "__main__":
    main()
