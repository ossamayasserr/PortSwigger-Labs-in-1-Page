############################################# Get All Labs Links #############################################

import requests
from bs4 import BeautifulSoup

# Define the URL you want to scrape
URL = "https://portswigger.net"

# Send an HTTP GET request to the URL
res = requests.get(URL+'/web-security/all-labs')
labLinks = list()
# Check if the request was successful (status code 200)
if res.status_code == 200:
    # Parse the HTML content of the page using Beautiful Soup
    soup = BeautifulSoup(res.text, 'html.parser')
    labElements = soup.find_all(class_="widgetcontainer-lab-link")
    print(f"Count of Lab Elements: {len(labElements)}")

    for e in labElements:
        link = URL + e.find_all('a')[0].get('href')
        labLinks.append(link)
    print(f"Count of Lab Links: {len(labElements)}")
else:
    print("Failed to retrieve the web page. Status code:", res.status_code)


############################################# Downloading All Labs #############################################

import os
import requests

# Specify the folder where you want to save the downloaded files
download_folder = 'labs/'

# Create the download folder if it doesn't exist
os.makedirs(download_folder, exist_ok=True)

# Function to generate a unique filename
def get_unique_filename(url, topCounter):
    base = str(topCounter) + " - " + os.path.basename(url)
    ext = ".html"
    counter = 0
    filename = f"{base}{ext}"
    while os.path.exists(os.path.join(download_folder, filename)):
        counter += 1
        filename = f"{base}_{counter}{ext}"
    return os.path.join(download_folder, filename)

allFileNames = list()
topCounter = 1
for url in labLinks:
    response = requests.get(url)
    if response.status_code == 200:
        filename = get_unique_filename(url, topCounter)
        allFileNames.append(filename)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded and saved as {os.path.basename(filename)}")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")
    topCounter += 1

######################################### Adding All Labs to a file #########################################

import os
from bs4 import BeautifulSoup

# Define the folder containing the HTML files
folder_path = 'labs'

# Initialize an empty string to store the combined HTML content

final_html = ''
# Iterate over all files in the folder
counter = -1
for filename in allFileNames:
    counter += 1
    filename = filename.split('/')[-1]
    # Check if the file is an HTML file (you can add more file format checks)
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            # Parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(html_content, 'html.parser')
            soup = soup.find(class_="section theme-white")
            # print(soup.contents)
            EXPERT = "label-purple-small" in str(soup.contents)

            if EXPERT: continue

            deleteElement = soup.find(class_='share-right')
            if deleteElement: deleteElement.decompose()

            deleteElement = soup.find(class_='footer')
            if deleteElement: deleteElement.decompose()

            deleteElement = soup.find(class_='hidden pageloadingmask')
            if deleteElement: deleteElement.decompose()

            deleteElement = soup.find_all(class_='component-solution expandable-container')
            for e in deleteElement:
                if "Community solutions" in e.text:
                    e.decompose()
                    break
            # Append the modified HTML to the combined_html variable
            current_html = str(soup.prettify())
            current_html += "<hr>\n"
            current_html = current_html.replace("<details>", "<details open>")
            current_html = current_html.replace("href=\"/", "href=\"https://portswigger.net/")
            current_html = current_html.replace("</h1>", f"({labLinks[counter].split('/')[4]})" + "</h1>")
            final_html += current_html
            # print(combined_html)

# Read the HTML file
with open("ResultTemplate.html", 'r', encoding='utf-8') as file:
    html_content = file.read()

html_content = html_content.replace("{{ content }}", final_html)
# Define the path to the output file
output_file = 'PortSwiggerAllLabs.html'

# Write the combined HTML to the output file
with open(output_file, 'w', encoding='utf-8') as output:
    output.write(html_content)

print(f'Combined HTML content written to {output_file}')
