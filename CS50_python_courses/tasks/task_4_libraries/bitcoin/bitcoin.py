import sys
import requests

def main():
    # Verify that the user provided at least one command-line argument (the amount of Bitcoin)
    if len(sys.argv) < 2:
        sys.exit("Missing command-line argument")

    try:
        # Attempt to convert the first command-line argument from a string to a float
        bitcoins = float(sys.argv[1])
    # Handle the error if the user passed text that cannot be converted into a number
    except ValueError:
        sys.exit("Command-line argument is not a number")

    # Define the authentication key and API endpoint URL for CoinCap
    api_key = "d41ec6269e347962c79c2906ebb64fabf5daedcaa1d9db7b1fb89990e348e580"
    url = f"https://rest.coincap.io/v3/assets/bitcoin?apiKey={api_key}"

    try:
        # Send an HTTP GET request to the CoinCap API endpoint
        response = requests.get(url)
         # Raise an HTTPError if the request returned an unsuccessful status code (e.g., 404, 500)
        response.raise_for_status()

        # Parse the response body as JSON into a Python dictionary
        data_json = response.json()

        # Extract the price of Bitcoin in USD from the nested dictionary structure and convert to float
        price_usd = float(data_json["data"]["priceUsd"])

    # Catch network-related issues (timeout, connection failure, bad status codes)
    except requests.RequestException:
        sys.exit("An error occurred while requesting the Bitcoin price API")
    # Catch structural errors if the API JSON data does not have the expected keys or formats
    except (KeyError, TypeError, ValueError):
        print("JSON received from API:", data_json)
        sys.exit("Error parsing the API response data")

    # Calculate the total value by multiplying the user's Bitcoin amount by the unit price
    total_cost = bitcoins * price_usd

    # Print the result formatted with commas for thousands and rounded to four decimal places
    print(f"${total_cost:,.4f}")

if __name__ == "__main__":
    main()
