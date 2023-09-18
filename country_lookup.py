import argparse
import requests
import json

def fetch_country_data():
    try:
        response = requests.get("https://www.travel-advisory.info/api")
        response.raise_for_status()
        data = response.json()
        return data.get("data", {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return {}

def lookup_country(country_code, country_data):
    if country_code in country_data:
        return country_data[country_code]["name"]
    else:
        return f"Country code '{country_code}' not found."

def main():
    parser = argparse.ArgumentParser(description="Lookup country names by country code.")
    parser.add_argument("--countryCodes", nargs="+", help="List of country codes to lookup", required=True)
    args = parser.parse_args()

    country_data = fetch_country_data()

    if not country_data:
        return

    results = {}
    for country_code in args.countryCodes:
        country_name = lookup_country(country_code, country_data)
        results[country_code] = country_name

    # Save the data to a JSON file
    with open("data.json", "w") as file:
        json.dump(results, file, indent=2)

    # Display the results
    for country_code, country_name in results.items():
        print(f"{country_code}: {country_name}")

if __name__ == "__main__":
    main()
