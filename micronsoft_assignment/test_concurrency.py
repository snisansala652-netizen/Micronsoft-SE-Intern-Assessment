import threading
import requests
import time

# The API endpoint for purchasing an item
# Ensure your Django server is running at this address
URL = "http://127.0.0.1:8000/api/purchase/"

def make_request(thread_id):
    """
    Simulates a single user attempt to purchase a product.
    """
    # Using product_id 1 which we initialized in the database
    payload = {"product_id": 1} 
    
    try:
        # Sending a POST request to the purchase API
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            # Successful purchase
            print(f"Thread {thread_id}: Success - {response.json()}")
        elif response.status_code == 400:
            # Likely out of stock
            print(f"Thread {thread_id}: Failed (Out of Stock) - {response.json()}")
        else:
            # Server or logic error
            print(f"Thread {thread_id}: Error (Status {response.status_code}) - {response.json()}")
            
    except Exception as e:
        # Connection issues (e.g., server not running)
        print(f"Thread {thread_id}: Connection Error - {e}")

def run_concurrency_test():
    """
    Spawns multiple parallel threads to simulate simultaneous user activity.
    """
    threads = []
    # Number of concurrent users to simulate
    # You can increase this to 100 once you verify it works for 10
    number_of_concurrent_users = 10 
    
    print(f"--- Starting Concurrency Test with {number_of_concurrent_users} users ---")
    start_time = time.time()

    # Initialize and start all threads simultaneously
    for i in range(number_of_concurrent_users):
        t = threading.Thread(target=make_request, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all users to finish their requests before ending the script
    for t in threads:
        t.join()

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    print(f"--- Test Completed in {duration} seconds ---")

if __name__ == "__main__":
    run_concurrency_test()