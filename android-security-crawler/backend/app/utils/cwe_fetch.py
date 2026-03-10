import nvdlib
import concurrent.futures
import csv
import time
from typing import List, Dict, Optional
import pandas as pd
import random
import os

def fetch_cwe_with_retry(
    cve_id: str,
    api_key: Optional[str] = None,
    max_retries: int = 6,
    base_delay: float = 1.0
) -> List[Dict]:
    """
    Fetch CWE categories for a single CVE ID with exponential backoff retry.
    
    :param cve_id: The CVE ID (e.g., 'CVE-2017-0144')
    :param api_key: Optional NVD API key for higher rate limits
    :param max_retries: Maximum number of retry attempts
    :param base_delay: Initial delay in seconds for backoff
    :return: List of CWE dictionaries for the CVE
    """
    delay = 6.0 # Default delays per NVD guidelines
    
    for attempt in range(max_retries):
        try:
            # Fetch the CVE using nvdlib
            results = nvdlib.searchCVE(
                cveId=cve_id,
            )
            if results:
                return results[0].cwe  # Return the list of CWE dicts
            else:
                raise ValueError(f"No data found for {cve_id}")
        except Exception as e:
            print(e)
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to fetch CWE for {cve_id} after {max_retries} attempts: {e}")
            
            # Exponential backoff: delay = base_delay * 2^attempt
            backoff_delay = base_delay * (2 ** attempt) * (random.randint(1,3))
            print(f"Attempt {attempt + 1} failed for {cve_id}: {e}. Retrying in {backoff_delay:.2f}s...")
            time.sleep(backoff_delay)
    
    return []  # Fallback empty list

def fetch_all_cwes_parallel(
    cve_ids: List[str],
    api_key: Optional[str] = None,
    max_workers: int = 5
) -> Dict[str, List[Dict]]:
    """
    Fetch CWE categories for a list of CVE IDs in parallel using a thread pool.
    
    :param cve_ids: List of CVE IDs to fetch
    :param api_key: Optional NVD API key
    :param max_workers: Maximum number of concurrent threads (respect NVD rate limits)
    :return: Dictionary mapping CVE ID to its CWE list
    """
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_cve = {
            executor.submit(fetch_cwe_with_retry, cve_id, api_key): cve_id
            for cve_id in cve_ids
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_cve):
            cve_id = future_to_cve[future]
            try:
                results[cve_id] = future.result()
                print(f"Successfully fetched CWE for {cve_id}")
            except Exception as e:
                print(f"Failed to fetch CWE for {cve_id}: {e}")
                results[cve_id] = []
    
    return results

def save_cwes_to_csv(cwes_data: Dict[str, List[Dict]], filename: str = "cve_cwe_data.csv"):
    """
    Save the fetched CWE data to a CSV file.
    Each row represents a CVE-CWE pair, with columns: CVE_ID, CWE_ID, CWE_Name.
    
    :param cwes_data: Dictionary mapping CVE ID to list of CWE dicts
    :param filename: Output CSV filename
    """
    if not cwes_data:
        print("No data to save.")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['CVE_ID', 'CWE_ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for cve_id, cwes in cwes_data.items():
            # print(type(cwes))
            if cwes:
                for cwe in cwes:
                    # print(cwe.value)
                    writer.writerow({
                        'CVE_ID': cve_id,
                        'CWE_ID': cwe.value,
                    })
            else:
                # Write a row for CVEs with no CWEs
                writer.writerow({
                    'CVE_ID': cve_id,
                    'CWE_ID': 'None',
                    # 'CWE_Name': 'No CWEs found'
                })
    
    print(f"Data saved to {os.path.abspath(filename)}")

# Example usage
if __name__ == "__main__":
    # Replace with your list of CVE IDs
    data = pd.read_csv("cve_data.csv")
    cve_list = data['id'].tolist()
    
    # Optional: Set your NVD API key (get one free from https://nvd.nist.gov/developers/request-an-api-key)
    api_key = None  # e.g., "your-api-key-here"
    
    # Fetch in parallel
    cwes_data = fetch_all_cwes_parallel(cve_list, max_workers=6)
    
    # Print results
    save_cwes_to_csv(cwes_data)
    # for cve_id, cwes in cwes_data.items():
    #     print(f"\nCWE for {cve_id}:")
    #     for cwe in cwes:
    #         print(f"  - {cwe.get('id', 'Unknown')}: {cwe.get('name', 'No name')}")
