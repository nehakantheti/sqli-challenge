import requests
import time

URL = "http://localhost:5000/check-pin"  # Update this if needed

for pin in range(3330, 3340):
    pin_str = f"{pin:04d}"  # Format as 4-digit string (e.g., "0001")

    try:
        response = requests.post(
            URL,
            json={"pin": pin_str},
            headers={"Content-Type": "application/json"}
        )

        data = response.json()
        print(data)

        if data.get("status") == "success":
            print(f"[✅] PIN found: {pin_str}")
            print(f"Response: {data}")
            break
        else:
            print(f"[❌] Tried: {pin_str} => {data.get('message')}")

    except Exception as e:
        print(f"[⚠️] Error on PIN {pin_str}: {e}")
        # time.sleep(1)  # Sleep to avoid hammering server on failure
