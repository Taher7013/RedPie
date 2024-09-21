import urllib.parse

def url_encoder(url):
    encoded_url = urllib.parse.quote(url)
    return encoded_url

# Example usage:
original_url = input("Enter URL Code to Encode : ")
encoded_url = url_encoder(original_url)
print("Encoded URL:", encoded_url)

