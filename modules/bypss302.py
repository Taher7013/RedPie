import requests

def fetch_url_no_redirect(url):
    try:
        response = requests.get(url, allow_redirects=False)
        if response.status_code == 302:
            print('[*] 302 Redirect Found !')
            redirect_url = response.headers['Location']
            print("Redirect URL:", redirect_url)
            return redirect_url
        else:
            print("Response Code:", response.status_code)
            print("Response content:", response.text)
            return response
    except requests.RequestException as e:
        print("An Error occurred:", e)
        return None


url = input("Enter URL To Fetch: ")
fetch_url_no_redirect(url)
