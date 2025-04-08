
# Data_engineering_Problem_2-
# VoIP Call Calculation from IPDR

This project processes IPDR (IP Detail Records) data to calculate and classify audio and video calls based on specific criteria. The calculations are performed based on various attributes such as MSISDN, domain, start time, end time, and volumes (UL and DL).

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Output](#output)
7. [License](#license)

## Overview

This script reads IPDR data from an Excel file, processes it, and calculates the total duration, volume, bit rate, and categorizes each call as an audio or video call. The data is filtered based on specified start and end date ranges, and the output is saved in an Excel file.

## Features

- **Call Duration Calculation**: Calculates the total duration of each call after excluding idle time (10 minutes).
- **Bitrate Calculation**: Computes the bitrate in Kbps for each call based on the total volume (UL + DL) and the total duration.
- **Audio/Video Classification**: Classifies the calls as `Audio` or `Video` based on bitrate thresholds.
- **Data Filtering**: Filters data based on MSISDN, domain, and a specific date range.
- **Output**: Generates an Excel file with calculated results, including MSISDN, domain, duration, bitrate, and call type (audio/video).

## Requirements

- Python 3.x
- pandas
- openpyxl (for reading and writing Excel files)
- datetime

To install the required dependencies, you can use the following command:

```bash
pip install pandas openpyxl
```

## Installation

1. Clone the repository or download the script to your local machine.

```bash
git clone https://github.com/Katleho-bob/Data_engineering_Problem_2-.git
cd Data_engineering_Problem_2
```

2. Install the necessary Python libraries:

```bash
pip install pandas openpyxl
```

3. Make sure your IPDR data is in an Excel file (`ipdr_data.xlsx`) that contains the following columns:
   - `msisdn` (MSISDN)
   - `domain` (VoIP app/domain)
   - `starttime` (start time of the call)
   - `endtime` (end time of the call)
   - `ulvolume` (upload volume in bytes)
   - `dlvolume` (download volume in bytes)

## Usage

1. Prepare your IPDR data in the specified Excel format.
2. Modify the script (if needed) to specify the path to your IPDR data file (`ipdr_data.xlsx`).
3. Run the script:

```bash
python voip_call_calculation.py
```

4. The script will process the IPDR data and generate an output Excel file (`voip_calls_summary_filtered.xlsx`) containing the calculated results.

## Output

The output Excel file will contain the following columns:

- `msisdn`: MSISDN of the call
- `domain`: VoIP app/domain name
- `duration_sec`: Duration of the call in seconds
- `fdr_count`: Number of FDRs (Call Detail Records) that make up a single call
- `kbps`: Bitrate of the call in Kbps
- `isAudio`: Boolean value indicating if the call is an audio call (`True`/`False`)
- `isVideo`: Boolean value indicating if the call is a video call (`True`/`False`)

### Example Output:

| msisdn      | domain  | duration_sec | fdr_count | kbps  | isAudio | isVideo |
|-------------|---------|--------------|-----------|-------|---------|---------|
| 1234567890  | WhatsApp | 120          | 3         | 150   | True    | False   |
| 9876543210  | Skype    | 300          | 5         | 250   | False   | True    |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

