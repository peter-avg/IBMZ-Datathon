import asyncio
import httpx

# The base URL of your running FastAPI application
BASE_URL = "https://ibm-datathon-api-gateway.onrender.com"

async def run_tests():
    """
    An async function to test creating and reading doctors.
    """
    # Use an async client to make requests
    async with httpx.AsyncClient() as client:
        
        # --- Test 1: Write Query (POST /doctor/) ---
        print("--- Running WRITE test ---")
        
        # The data for the new doctor we want to create
        # new_doctor_data = {
        #     "full_name": "Dr. Niket Ganatra",
        # }
        
        # try:
        #     # Send the POST request to the /doctor/ endpoint
        #     response = await client.post(f"{BASE_URL}/create_doctor/", json=new_doctor_data)
            
        #     # Raise an error if the request was unsuccessful (e.g., 4xx or 5xx)
        #     response.raise_for_status()
            
        #     # Print the successful response from the server
        #     created_doctor = response.json()
        #     created_doctor_id = created_doctor.get("doctor_id")
        #     print("✅ Successfully created doctor:")
        #     print(created_doctor)
            
        # except httpx.HTTPStatusError as e:
        #     print(f"❌ Error creating doctor: {e.response.status_code}")
        #     print(f"   Response: {e.response.text}")
        # except httpx.RequestError as e:
        #     print(f"❌ A network error occurred: {e.request.url!r}.")
        #     return # Stop if we can't connect

        # print("\n" + "="*30 + "\n")

        # --- Test 2: Read Query (GET /doctor/) ---
        print("--- Running READ test ---")
        
        try:
            # Send the GET request to the /doctor/ endpoint
            response = await client.get(f"{BASE_URL}/doctors/")
            response.raise_for_status()
            
            all_doctors = response.json()
            print(f"✅ Successfully retrieved {len(all_doctors)} doctors:")
            
            # Print all retrieved doctors
            for doctor in all_doctors:
                print(doctor)
                
        except httpx.HTTPStatusError as e:
            print(f"❌ Error reading doctors: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        except httpx.RequestError as e:
            print(f"❌ A network error occurred: {e.request.url!r}.")

        
        # # --- 3. DELETE Test ---
        # if created_doctor_id:
        #     print(f"--- Running DELETE test for ID: {created_doctor_id} ---")
        #     try:
        #         # Send the DELETE request to the /doctor/{doctor_id} endpoint
        #         response = await client.delete(f"{BASE_URL}/doctor/{created_doctor_id}")
        #         response.raise_for_status()
        #         print("✅ Successfully deleted doctor.")
        #     except httpx.HTTPStatusError as e:
        #         print(f"❌ Error deleting doctor: {e.response.status_code}")
        #         print(f"   Response: {e.response.text}")

        print("\n" + "="*30 + "\n")

# Run the async test function
if __name__ == "__main__":
    asyncio.run(run_tests())