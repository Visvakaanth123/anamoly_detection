import json
import re

logs = []

with open("F:/project 2/logs/winlog.0", "r", encoding="utf-8") as f:
    for line in f:
        # Extract JSON part using regex
        match = re.search(r'\[(\d+\.\d+),\s*(\{.*\})\]', line)
        if match:
            timestamp = float(match.group(1))
            try:
                log_data = json.loads(match.group(2))
                log_data['timestamp'] = timestamp
                logs.append(log_data)
            except json.JSONDecodeError:
                pass

print(f"Loaded {len(logs)} log entries")
print(logs[0])


import pandas as pd
df = pd.DataFrame(logs)
df = df.drop(columns=[
    "ComputerName", "Data", "Message", "StringInserts", "Sid", "TimeGenerated", "TimeWritten"
])
df = pd.get_dummies(df, columns=["EventType", "Channel", "SourceName"])
print(df.columns)


from sklearn.ensemble import IsolationForest
model = IsolationForest(contamination=0.01,random_state=42)
model.fit(df)
df['anamoly'] = model.predict(df)




anomalies = df[df['anamoly'] == -1]
print(f"Detected number of anamolies {len(anomalies)} out of {len(df)}")

# Step 2: Select meaningful columns
columns_to_display = [
    'RecordNumber', 'EventID', 'EventType_Warning',
    'Channel_Setup', 'SourceName', 'timestamp'
]

# If you have the original JSON log loaded in a variable `logs` (a list of dicts)
# and you used that to build the DataFrame `df`, you can map back like this:
for idx in anomalies.index[:5]:  # limit to first 5 anomalies
    log = logs[idx]  # Assuming logs[idx] gives the original log dictionary
    print(f"\n Record {log['RecordNumber']} | EventID: {log['EventID']}")
    print(f" TimeGenerated: {log['TimeGenerated']}")
    print(f" Channel: {log['Channel']} | Source: {log['SourceName']}")
    print(f" EventType: {log['EventType']}")
    print(f" Message: {log['Message'][:200] if log['Message'] else 'No message provided'}")
    print("  Anomaly detected due to rare combination or missing data.")