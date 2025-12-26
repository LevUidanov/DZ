import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    # === СБОР ДАННЫХ ===
    data = scrape_countries()
    print(f"\nСобрано стран: {len(data)}")

    if not data:
        print("Нет данных для анализа")
        return

    df = pd.DataFrame(data)

    # === СОХРАНЕНИЕ CSV ===
    df.to_csv("countries_dataset.csv", index=False, encoding="utf-8")
    print("CSV сохранён: countries_dataset.csv")

    # === EDA ===
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

    # === ГИСТОГРАММА + KDE (ЛОГАРИФМИЧЕСКАЯ ШКАЛА) ===
    plt.figure(figsize=(8, 5))

    # убираем нули, логарифм от 0 невозможен
    pop_log = df[df["population"] > 0]["population"]

    sns.histplot(
        pop_log,
        bins=20,
        kde=True,
        color="skyblue",
        log_scale=True
    )

    plt.title("Распределение численности населения стран (логарифмическая шкала)")
    plt.xlabel("Численность населения (лог шкала)")
    plt.ylabel("Количество стран")

    plt.tight_layout()
    plt.savefig("population_distribution_log.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
