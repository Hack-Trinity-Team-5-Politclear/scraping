import csv
import requests
import json
from datetime import datetime

def read_tsv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        rows = list(tsv_reader)
    return rows

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def get_latest_entries(rows, count=40):
    # Extract date and filter out rows with invalid dates
    rows_with_date = [(row, parse_date(row[5])) for row in rows]
    valid_rows_with_date = [row for row in rows_with_date if row[1] is not None]

    # Sort by date
    valid_rows_with_date.sort(key=lambda x: x[1], reverse=True)

    # Select latest entries
    latest_entries = [row for row, date in valid_rows_with_date[:count]]
    return latest_entries

def summarize_entries(entries):
    # Placeholder for summarization
    sum = []

    for entry in entries:
        # print(entry[10])
        resp = gpt4summarise(entry[10])
        sum.append(resp)
        print(resp)


    with open("data/summarise-out.json", 'w') as file:
        json.dump(sum, file, indent=4)

    summaries = ["Placeholder summary for: " + entry[0] for entry in entries]
    return summaries


def gpt4summarise(text):
    url = "https://api.openai.com/v1/chat/completions"

    payload = json.dumps({
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are going to summarise the text provided by the user into one single paragraph."
            },
            {
                "role": "user",
                "content": "Below is a statement made by a TD in Ireland. Summarise it and take away key points: " + text
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()["choices"][0]["message"]["content"]

def main():
    file_path = './data/Chris-Andrews.D.2007-06-14_limit5000.tsv'
    rows = read_tsv(file_path)
    latest_entries = get_latest_entries(rows)
    summaries = summarize_entries(latest_entries)
    return summaries

if __name__ == "__main__":
    summarized_data = main()
    print(summarized_data)
