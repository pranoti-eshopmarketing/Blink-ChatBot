from solders.keypair import Keypair as SoldersKeypair
import base58
from solana.rpc.api import Client
from solana.constants import Pubkey
import requests

url = "https://quote-api.jup.ag/v6/quote"

def create_solana_wallet():
    # Generate a new keypair using Solders
    keypair = SoldersKeypair()

    # Get the public key (address)
    public_key = bytes(keypair.pubkey())
    # Get the secret key (private key)
    secret_key = keypair.secret()
    
    #combined key
    combined_key = secret_key + public_key

    # Display the public key
    print(f"Public Key: {keypair.pubkey()}")
    private_key = base58.b58encode(combined_key).decode()
    # Encode the secret key in Base58
    # private_key_base58 = base58.b58encode(secret_key).decode('utf-8')
    print(f"Private Key: {private_key}")

    # Return the keypair for further use
    return [keypair.pubkey(), private_key]

def buy_solana(token_address):
    print(token_address)
    # URL for Jupiter API
    jupiter_api_url = "https://quote-api.jup.ag/v1/quote"
    
    # Define parameters for the Jupiter API
    payload = {
        
    }
    
    headers = {
        'Accept': 'application/json'
    }
    
    try:
        # Make the GET request with SSL verification disabled
        response = requests.get(jupiter_api_url, headers=headers, data=payload)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse and print the JSON response
        data = response.json()
        print("Jupiter API Response:", data)
        return data
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def price(token_address):
    # Base URL with the dynamic token address
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"

    try:
        # Making a GET request to the API
        response = requests.get(url)

        # Checking if the request was successful
        if response.status_code == 200:
            # Parsing the JSON response
            data = response.json()
            print("dataaaaaaaaaa", data['pairs'][0])
            return data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
