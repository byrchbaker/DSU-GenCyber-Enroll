# import some stuff
import subprocess
import requests, pytz, time, browser_cookie3, psutil, sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Define the URLs for each period
period_urls = [
    "https://go.gencyber.camp/electives?period=1",
    "https://go.gencyber.camp/electives?period=2",
    "https://go.gencyber.camp/electives?period=3"
]

def checkChrome(): 
    # See if chrome is running currently
    for proc in psutil.process_iter():
        if proc.name() == "chrome.exe":
            print("Chrome is running. Please close chrome completely before continuing with the auto elective script.")
            exit()

def clear_console():
    # Clear console command for different operating systems
    command = ""

    if sys.platform.startswith('win'):
        command = 'cls'  # For Windows
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        command = 'clear'  # For Linux and macOS

    # Execute the console clear command
    if command:
        _ = sys.stdout.write('\033[2J\033[H')  # ANSI escape sequence for clearing console
        _ = sys.stdout.flush()
        _ = sys.stderr.write('\033[2J\033[H')
        _ = sys.stderr.flush()
        _ = subprocess.call(command, shell=True)


def getRememberCookie(domain='go.gencyber.camp',cookieName='remember_token'):

    Cookies={}
    chromeCookies = list(browser_cookie3.chrome())

    for cookie in chromeCookies:
        if (domain in cookie.domain):
            Cookies[cookie.name]=cookie.value

    if(cookieName!=''):
        try:
            return Cookies[cookieName] 
        except:
            return {} 
    else:
        return Cookies 

def check_login_credentials():
    
    url = "https://go.gencyber.camp/completions"

    session = requests.Session()
    session.cookies.set("remember_token", getRememberCookie())

    response = session.get(url)

    if response.status_code == 200:
        if "My Completions and Progress" in response.text:
            print("Connection successful!")
        else:
            print("Login not successful! Check your cookies!")
            exit()
    else:
        print("Connection failed with status code:", response.status_code)


# Function to parse the elective information from HTML
def parse_elective_info(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article", class_="media content-section")
    electives = []

    for article in articles:
        # ill never be doing this again
        name = article.find("h2").text.strip()
        description = article.find("p", class_="article-content").text.strip().replace("Description: ", "")
        instructor = article.find("a", class_="mr-2").text.strip()
        location = article.find_all("p", class_="article-content")[1].text.strip().replace("Location: ", "")
        url = article.find("button", class_="btn btn-outline-success")["onclick"].replace("window.location.href = '", "").replace("'", "")
        electives.append({"name": name, "description": description, "instructor": instructor, "location": location, "url": url})

    return electives


# Function to register for an elective using the provided URL
def register_for_elective(url):
    base_url = "https://go.gencyber.camp"
    register_url = base_url + url
    
    session = requests.Session()
    session.cookies.set("remember_token", getRememberCookie())
    
    response = session.get(register_url)

    if response.status_code == 200:
        # Check if the expected content or response headers indicate success
        if "Elective Registration Successful" in response.text:
            print(f"\nSuccessfully registered for elective: {url}")
        else:
            print(f"\nFailed to registered for elective: {url}")
    else:
        print("Connection failed with status code:", response.status_code)

# Function to countdown to a specific time
def countdown_to_time():
    while True:
        # Send GET request to the API
        response = requests.get("https://go.gencyber.camp/api/regtime")
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            starttime = data.get("starttime")
            
            # Convert the start time to a datetime object
            start_datetime = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
            
            # Get the current time
            current_datetime = datetime.now()
            
            # Calculate the time difference
            time_difference = start_datetime - current_datetime
            
            # Check if it's time to start
            if time_difference.total_seconds() <= 0:
                break
                # ... continue to the registering of electives
            
            # Calculate the time to sleep in seconds
            sleep_time = time_difference.total_seconds()
            minutes, seconds = divmod(sleep_time, 60)
            hours, minutes = divmod(minutes, 60)
            sys.stdout.write(
                "\rWaiting for {:02.0f}h {:02.0f}m {:02.0f}s until electives open up...".format(
                    hours, minutes, seconds
                )
            )
            sys.stdout.flush()
            
            # Sleep for 1 second before checking again
            time.sleep(.5)
        else:
            print("Failed to retrieve the start time. Retrying...")
            time.sleep(5)


# Main script
if __name__ == "__main__":
    # Display the electives for each period
    elective_urls = []
    elective_names = []
    # empty.... just like my soul
    checkChrome()
    check_login_credentials()
    
    for i, period_url in enumerate(period_urls, start=1):
        response = requests.get(period_url)
        if response.ok:
            electives = parse_elective_info(response.text)
            print(f"\nElectives for Period {i}:")
            for j, elective in enumerate(electives, start=1):
                print(f"{j}. {elective['name']} - {elective['description']} - {elective['instructor']} - {elective['location']} \n")
        else:
            print(f"Failed to fetch period URL: {period_url}")

        # Wait for user input to select an elective
        selected_elective = input("Select an elective number to register (or enter 'skip' to move to the next period): ")
        
        if selected_elective.lower() == "skip":
            print("Moving to the next period...")
            continue
        
        try:
            selected_elective = int(selected_elective)
            if selected_elective < 1 or selected_elective > len(electives):
                print("Invalid elective number. Moving to the next period...")
                continue
        except ValueError:
            print("Invalid input. Moving to the next period...")
            continue
        
        
        
        # Register for the selected elective
        elective_url = electives[selected_elective - 1]['url']  # Assuming each elective has a unique URL
        elective_urls.append(elective_url)
        elective_name = electives[selected_elective - 1]['name']
        elective_names.append(elective_name)
        
        
    # Clear the console
    clear_console()

    # Display the selected electives
    print("Selected Electives:")
    for elective_name in enumerate(elective_names):
        print(f"{elective_name} \n")
    
    # Perform the countdown
    countdown_to_time()
    
    # Register for all the electives
    for elective_url in elective_urls:
       register_for_elective(elective_url)

    print("Registration process completed.")
