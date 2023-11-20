# DataDog Logs Exclusion Filters Audit

This script retrieves and prints the list of enabled exclusion filters for a specified DataDog Logs Index. 
It excludes filters with certain name patterns and saves the final printing result to a file.
Target Path: https://app.datadoghq.com/logs/pipelines/indexes

## Architecture Diagram
![_finops_3.png](..%2Fdoc%2F_finops_3.png)

## Prerequisites

- Python 3.x
- `datadog_api_client` library (install via `pip3 install datadog_api_client`)
- `webexteamssdk` library

## Usage

1. Clone the repository or download the script.
2. Install the required dependencies: `pip3 install datadog_api_client`.
3. Run the command: `python3 audit_dd_exclusion_filters_of_indexed_logs.py --api-key ***  --app-key *** --webex-token *** --room-id ***`.

## Example of Output 

`$ python3 audit_dd_exclusion_filters_of_indexed_logs.py --api-key ***  --app-key *** --webex-token *** --room-id ***`
```
    Warning! 
DataDog Costs might be affected! 
Please, check the List of enabled non-Prod Rules for Indexed Logs:
    3. Allow QA Fluentd logs from Dev EKS
    21. Exclude duplicating log in application
Final printing result saved to list_output.txt
```

## Notes
Please create QA\DEV Rules with name pattern "DEV_your_name".
Please do not modify Rules with name patterns ["Prod", "Stage", "Perf"]

## Reference

- https://github.com/DataDog/datadog-api-client-python/
- https://datadoghq.dev/datadog-api-client-python/index.html
- https://docs.datadoghq.com/api/latest/logs-indexes/