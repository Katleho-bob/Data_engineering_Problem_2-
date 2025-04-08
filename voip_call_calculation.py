import pandas as pd
from datetime import timedelta

# Read Excel file
# data = pd.read_excel("ipdr_data.xlsx", parse_dates=['starttime', 'endtime'])
data = pd.read_excel("ipdr_data.xlsx")

# Convert starttime and endtime to datetime objects
data['starttime'] = pd.to_datetime(data['starttime'], format="%Y-%m-%d%H:%M:%S")
data['endtime'] = pd.to_datetime(data['endtime'], format="%Y-%m-%d%H:%M:%S")

# Define your date range for filtering (adjust as needed)
start_date = "2021-01-01"
end_date = "2025-12-31"
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Filter data based on the specified start and end datetime
data = data[(data['starttime'] >= start_datetime) & (data['endtime'] <= end_datetime)]

# Convert UL and DL volume from bytes to kilobytes
data['ulvolume_kb'] = data['ulvolume'] / 1024
data['dlvolume_kb'] = data['dlvolume'] / 1024

# Sort records for consistent grouping
data.sort_values(by=['msisdn', 'domain', 'starttime'], inplace=True)

# Group records by msisdn and domain
grouped_calls = []
call_id = 0

for (msisdn, domain), group in data.groupby(['msisdn', 'domain']):
    group = group.reset_index(drop=True)
    current_call = [group.loc[0]]
    
    for i in range(1, len(group)):
        gap = (group.loc[i, 'starttime'] - group.loc[i - 1, 'endtime']).total_seconds()
        if gap <= 600:  # Less than or equal to 10 minutes
            current_call.append(group.loc[i])
        else:
            grouped_calls.append((msisdn, domain, current_call))
            current_call = [group.loc[i]]
    
    grouped_calls.append((msisdn, domain, current_call))

# Process each grouped call
results = []

for msisdn, domain, records in grouped_calls:
    call_df = pd.DataFrame(records)
    
    # Adjust ET by removing idle time (10 min), if applicable
    call_df['adjusted_et'] = call_df['endtime'] - timedelta(minutes=10)
    call_df['adjusted_et'] = call_df.apply(
        lambda row: row['endtime'] if row['adjusted_et'] < row['starttime'] else row['adjusted_et'],
        axis=1
    )

    start_time = call_df['starttime'].min()
    end_time = call_df['adjusted_et'].max()
    duration_sec = (end_time - start_time).total_seconds()

    total_volume_kb = call_df['ulvolume_kb'].sum() + call_df['dlvolume_kb'].sum()
    bitrate_kbps = total_volume_kb / duration_sec if duration_sec > 0 else 0

    is_audio = False
    is_video = False
    if bitrate_kbps >= 10:
        is_audio = bitrate_kbps <= 200
        is_video = bitrate_kbps > 200

        results.append({
            'msisdn': msisdn,
            'domain': domain,
            'duration_sec': int(duration_sec),
            'fdr_count': len(call_df),
            'kbps': round(bitrate_kbps, 2),
            'isAudio': is_audio,  # Boolean value
            'isVideo': is_video   # Boolean value
        })

# Save result to Excel or display
output_df = pd.DataFrame(results)

# Save the output to an Excel file
output_df.to_excel("voip_calls_summary_filtered.xlsx", index=False)

# Display message after processing
print("✅ VoIP call calculation completed. Results saved to 'voip_calls_summary_filtered.xlsx'.")
