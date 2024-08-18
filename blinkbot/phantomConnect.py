from solders.keypair import Keypair as SoldersKeypair
import base58

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

