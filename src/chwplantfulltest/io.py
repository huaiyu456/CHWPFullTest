import csv


def load_csv_data(csv_path):
    data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            converted = {}
            for key, value in row.items():
                try:
                    converted[key] = float(value)
                except (TypeError, ValueError):
                    converted[key] = value
            data.append(converted)
    return data



