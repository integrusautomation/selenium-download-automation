#!/usr/bin/env python3
"""
Script to update webhook results from selenium script execution
This extracts the results from the selenium script logs and updates the webhook data
"""

import re
import json
import os
from datetime import datetime

def extract_results_from_log(log_content):
    """
    Extract the results dictionary from selenium script log content
    """
    # Look for the "Results by folder:" line in the log
    pattern = r"Results by folder:\s*({.*?})"
    match = re.search(pattern, log_content, re.DOTALL)
    
    if match:
        try:
            # Extract the dictionary string and evaluate it
            results_str = match.group(1)
            # Convert single quotes to double quotes for JSON parsing
            results_str = results_str.replace("'", '"')
            results = json.loads(results_str)
            return results
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing results: {e}")
            return None
    else:
        print("No results found in log content")
        return None

def update_webhook_data(results):
    """
    Update the webhook app with new results data
    """
    webhook_file = "webhook_app.py"
    
    if not os.path.exists(webhook_file):
        print(f"Webhook file {webhook_file} not found")
        return False
    
    # Read the current webhook file
    with open(webhook_file, 'r') as f:
        content = f.read()
    
    # Find the get_latest_results function and replace its return value
    pattern = r'(def get_latest_results\(\):.*?return ){.*?}'
    
    # Convert results to a properly formatted string
    results_str = json.dumps(results, indent=8)
    
    # Replace the return statement
    new_content = re.sub(
        pattern,
        f'\\1{results_str}',
        content,
        flags=re.DOTALL
    )
    
    # Write the updated content back
    with open(webhook_file, 'w') as f:
        f.write(new_content)
    
    print(f"Updated webhook with {len(results)} folders")
    return True

def main():
    """
    Main function to update webhook results
    """
    # This would typically read from a log file or database
    # For now, we'll use the sample data
    sample_results = {
        'zb3ZwQnVuZcM0cfCNbQoIQ/': ['000000108', '000000107', '000000106', '000000105', '000000104'],
        'EQl5K9ngclSt6QfdgqaWOQ/': ['000000078', '000000077', '000000076', '000000075', '000000074'],
        'TJOu2PU1eVE4ggj03EvmEA/': ['000000061', '000000060', '000000059'],
        'xOHNlQAHxXOCo0ZZ80tknw/': ['000000065', '000000064'],
        'MXQk7aMKOrU8tSrwloxHag/': ['000000067', '000000066', '000000065'],
        'MgZvDUNpAf59Z8nNKjY34A/': ['000000054', '000000053', '000000052'],
        'AKNx0zBYIaTBbjtKpVg0cg/': ['000000061', '000000060', '000000059'],
        'vMNFGGUkeJCcUm1bnF3kdA/': ['000000051', '000000050', '000000049'],
        'gmjimA9WCpHTavCT8Y99SA/': ['000000056', '000000055', '000000054'],
        'BQ5rCYhC0pU9sCYNvgfLsA/': ['000000048', '000000047', '000000046'],
        'rCQDjfbgNEgddzoNWR0Zcg/': ['000000051', '000000050', '000000049', '000000048'],
        'vmjDkWJaCiLXbkauYw7PeA/': ['000000051', '000000050'],
        'Exg68pTxujyr4xIaohT1dg/': ['000000050', '000000049'],
        'pnSRZsbrNUQqwuE9Q9Tv3g/': ['000000063', '000000062', '000000061', '000000060', '000000059'],
        '5THDQ1wnHRvIgGjIUlOqnA/': ['000000050', '000000049'],
        'Zy19AY3hC3sR7Q0USiwj5w/': ['000000063', '000000062', '000000061', '000000060', '000000059', '000000058'],
        'VdO01hDp4zkgO2Ylv6wgcw/': ['000000061', '000000060', '000000059'],
        'Ok85iau0YPhBTnFOfYarZw/': ['000000057', '000000056', '000000055', '000000054'],
        'FvXrHNoU0tpjCelYqbtD9w/': ['000000056', '000000055', '000000054', '000000053'],
        'hZrOXYcnbylwKmbsVs8lIA/': ['000000056', '000000055', '000000054', '000000053'],
        'JUTbwdhFNqk0kXFfJGGKwA/': ['000000072', '000000071', '000000070', '000000069', '000000068'],
        'OtXaEXl64gDGtW2saOXUZw/': ['000000047', '000000046', '000000045'],
        'R9sv2TMJTnlCnCdk9qdc3Q/': ['000000052', '000000051', '000000050', '000000049'],
        'ABlTscZ34q7CU6Z7p0TUwA/': [],
        'ObCLgchOb2aC6HnsMJIbVA/': ['000000063', '000000062', '000000061', '000000060'],
        'GRAuissfGi7K1CXeQBZvdA/': ['000000060', '000000059', '000000058', '000000057', '000000056'],
        '5HtkrOzkRZCoePzMvkJ3xg/': ['000000057', '000000056', '000000055', '000000054'],
        'IM475uNIONS7uu1kQEK2VQ/': ['000000057', '000000056', '000000055', '000000054'],
        'DQyuJyKAEmhGQcAoQ3x3Mg/': ['000000057', '000000056', '000000055'],
        'ouVVEl9JwUz0ws5gMRwLNQ/': ['000000050', '000000049'],
        'LVjsRgRzmpiyxuWNiOh0lg/': ['000000055', '000000054', '000000053', '000000052', '000000051'],
        's3pIL05Sqsfm2ScDllgbNQ/': ['000000048', '000000047', '000000046'],
        'AMbbNCwUNUX2nUUps9gN4A/': ['000000039', '000000038'],
        'c1b1iwXA4nmixk3DvytdiA/': ['000000054', '000000053', '000000052'],
        'XWAn6pOdfkaNZdmO71BgnA/': ['000000050', '000000049'],
        'gzYveUjjOx25gBJEoiHhEw/': ['000000050', '000000049', '000000048', '000000047'],
        'UJFc11Ho5o1QPJWNrwxhAQ/': ['000000052', '000000051', '000000050', '000000049'],
        'bUniiJRB1It6h3pE30CVfA/': ['000000039', '000000038'],
        'crao2Wv6h5ekVMM7ZInMQA/': ['000000055', '000000054', '000000053', '000000052'],
        'OtK4jH1u6DQMYE8451Lr8A/': ['000000051', '000000050', '000000049', '000000048'],
        '5HtrJ7DW9bYW9Drn5ud80g/': ['000000056', '000000055'],
        'eyMF34dqO3Te9a0Qu4zV4Q/': ['000000048', '000000047', '000000046'],
        '5NP6CL8Fak2PGWsn43Gp0g/': ['000000052', '000000051', '000000050', '000000049'],
        'NIhDkzseUi4XiGR4Yh8l7g/': ['000000060', '000000059', '000000058', '000000057'],
        'Q5GCRyHsM4GZJ4f1OYUkLA/': ['000000059', '000000058'],
        'Bj2hOTDCCbUSxiNX627Unw/': ['000000051', '000000050', '000000049'],
        'FClITJqal67ESpxWJglYjQ/': ['000000043', '000000042'],
        'vM06hslrVVQ3CmcEmisJ2w/': ['000000065', '000000064', '000000063', '000000062'],
        'VtrjgjQSxQkN2vCrTdvHoA/': ['000000052', '000000051', '000000050', '000000049'],
        'HaRj88fFDQql8W10JnGp5Q/': ['000000063', '000000062', '000000061', '000000060']
    }
    
    # Update the webhook with the results
    success = update_webhook_data(sample_results)
    
    if success:
        print("Webhook updated successfully!")
        print(f"Total folders: {len(sample_results)}")
        print(f"Total files: {sum(len(files) for files in sample_results.values())}")
    else:
        print("Failed to update webhook")
    
    return success

if __name__ == "__main__":
    main()
