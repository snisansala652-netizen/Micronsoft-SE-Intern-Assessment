import threading
import requests
import json

# The endpoint we created for purchase/checkout
URL = "http://127.0.0.1:8000/api/checkout/"

# Sample payload (Make sure product ID 1 exists in your DB with limited stock)
payload = {
    "items": [{"id": 1}] 
}

def make_request(thread_id):
    """Function to send a single POST request to the checkout API"""
    try:
        response = requests.post(
            URL, 
            data=json.dumps(payload), 
            headers={'Content-Type': 'application/json'}
        )
        print(f"Thread {thread_id}: Status {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Thread {thread_id}: Error - {e}")

def run_load_test(concurrent_requests=100):
    """Fires multiple concurrent threads to test race conditions"""
    threads = []
    
    print(f"🚀 Starting load test with {concurrent_requests} concurrent requests...")

    for i in range(concurrent_requests):
        t = threading.Thread(target=make_request, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("\n✅ Load test completed. Check your database stock and transaction records.")

if __name__ == "__main__":
    # Ensure your Django server is running before executing this
    run_load_test(100)