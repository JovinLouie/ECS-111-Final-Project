from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import undetected_chromedriver as uc
from random import uniform
from stem import Signal
from stem.control import Controller


players = pd.read_csv('valorant_players.csv')

# Function to change IP using Tor's ControlPort
def change_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        print("IP rotated")
        time.sleep(5)

#Initializing new columns (data that scraped will go here)
players['hs_percent'] = None
players['body_percent'] = None
players['leg_percent'] = None
players['s_damage_per_round'] = None
players['s_kd_ratio'] = None
players['s_hs_percent'] = None
players['s_win_percent'] = None
players['s_wins'] = None
players['s_kast_percent'] = None
players['s_dd_round'] = None
players['s_kills'] = None
players['s_deaths'] = None
players['s_assists'] = None
players['s_acs'] = None
players['s_kad_ratio'] = None
players['s_kills_per_round'] = None
players['s_first_bloods'] = None
players['s_flawless_rounds'] = None
players['s_aces'] = None

#Url to go to
def format_url(name,tag):
    return f"https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview"

#Initializing chrome driver, using the tor proxy server
options = uc.ChromeOptions()
options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
options.headless = False  # or False for testing
driver = uc.Chrome(options=options)

#Initializing tracker for when to change ip
count = 0
#Changing ip on startup of script in case a cloudflare block hits
change_ip()
try:
    for _, row in players.iterrows():
        if(count == 10):
            change_ip()
            count = 0

        #While loop for retrying the same user in case of a sleep hit
        while True:
            url = format_url(row['user'],row['tag'])
            print(f"Scraping {row['user']} -> {url}")
            try:
                driver.get(url)

                #Wait for the stats header or error message
                try:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//main"))
                    )

                    print("main exists")

                    try:
                        #Check for stats div
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'vppn')]"))
                        )

                        # Check for the profile private message text in the span
                        private_message_element = driver.find_element(By.XPATH, "//div[contains(@class, 'vppn')]//span[contains(text(), 'profile is private')]")

                        if private_message_element:
                            print(f"{row['user']} has a private profile. Skipping.")
                            break
                    except TimeoutException:
                        print("Not private, proceeding...")
                        pass
                    
                    try:
                        #Check if the "Player not found" message exists
                        player_not_found = driver.find_element(By.CSS_SELECTOR, 'h1.text-24.tl\\:text-32.font-bold.font-industry.uppercase.m-0')
                        if player_not_found.text.lower() == "player not found":
                            print(f"text is: {player_not_found.text.lower()}")
                            print(f"{row['user']} not found. Skipping.")
                            break

                        else:
                            #If the element exists but there's an error in the text, timeout for 10 minutes
                            print(f"Error in text for {row['user']}\n{player_not_found.text.lower()}. Sleeping 10 minutes.")
                            time.sleep(600)
                            driver.refresh()  # Perform a full refresh of the page
                            continue

                    except Exception as e:
                        # If not found, the element will raise an exception
                        print(f"{row['user']} found. Proceeding...")
                    
                    time.sleep(5)

                    #check for the stats
                    WebDriverWait(driver, 30).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'numbers')]"))
                    )

                    '''WebDriverWait(driver, 30).until(
                        EC.visibility_of_element_located((By.XPATH, "//table[contains(@class, 'accuracy__stats')]"))
                    )'''

                #If there's a timeout error then log the page_source, for checking what has loaded
                except TimeoutException:
                    print(f"Timeout — Couldn't grab expected elements for {row['user']}. Saving HTML and sleeping.")
                    with open(f"debug_{row['user']}.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)  # Save to investigate
                    break

                # Check if it's a private profile
                if driver.find_elements(By.XPATH, "//p[contains(text(), 'If this is your account, you can view your stats by logging in with your Riot account!')]"):
                    print(f"{row['user']} has a private profile. Skipping.")
                    continue

                #Side stats
                try:
                    hs_percent = driver.find_element(By.XPATH, "//tr[th[text()='Head']]/td[@class='stat']//span[@class='stat__value' and contains(text(), '%')]").text
                    players.at[_, 'hs_percent'] = hs_percent
                except:
                    players.at[_, 'hs_percent'] = None

                try:
                    body_percent = driver.find_element(By.XPATH, "//*[contains(text(), 'Body')]/following::span[contains(@class, 'stat__value')][1]").text
                    players.at[_, 'body_percent'] = body_percent
                except:
                    players.at[_, 'body_percent'] = None

                try:
                    leg_percent = driver.find_element(By.XPATH, "//tr[th[text()='Legs']]/td[@class='stat']//span[@class='stat__value' and contains(text(), '%')]").text
                    players.at[_, 'leg_percent'] = leg_percent
                except:
                    players.at[_, 'leg_percent'] = None
                
                # Giant stats 
                try:
                    s_damage_per_round = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[@class='name' and text()='Damage/Round']]//span[@class='value']").text
                    players.at[_, 's_damage_per_round'] = s_damage_per_round
                except:
                    players.at[_, 's_damage_per_round'] = None

                try:
                    s_kd_ratio = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='K/D Ratio']]//span[@class='value']").text
                    players.at[_, 's_kd_ratio'] = s_kd_ratio
                except:
                    players.at[_, 's_kd_ratio'] = None

                try:
                    s_hs_percent = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Headshot %']]//span[@class='value']").text
                    players.at[_, 's_hs_percent'] = s_hs_percent
                except:
                    players.at[_, 's_hs_percent'] = None

                try:
                    s_win_percent = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Win %']]//span[@class='value']").text
                    players.at[_, 's_win_percent'] = s_win_percent
                except:
                    players.at[_, 's_win_percent'] = None

                #General stats
                try:
                    s_wins = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Wins']]//span[@class='value']").text
                    players.at[_, 's_wins'] = s_wins
                except:
                    players.at[_, 's_wins'] = None

                try:
                    s_kast_percent = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='KAST']]//span[@class='value']").text
                    players.at[_, 's_kast_percent'] = s_kast_percent
                except:
                    players.at[_, 's_kast_percent'] = None

                try:
                    s_dd_round = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='DDΔ/Round']]//span[@class='value']").text
                    players.at[_, 's_dd_round'] = s_dd_round
                except:
                    players.at[_, 's_dd_round'] = None

                try:
                    s_kills = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Kills']]//span[@class='value']").text
                    players.at[_, 's_kills'] = s_kills
                except:
                    players.at[_, 's_kills'] = None

                try:
                    s_deaths = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Deaths']]//span[@class='value']").text
                    players.at[_, 's_deaths'] = s_deaths
                except:
                    players.at[_, 's_deaths'] = None

                try:
                    s_assists = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Assists']]//span[@class='value']").text
                    players.at[_, 's_assists'] = s_assists
                except:
                    players.at[_, 's_assists'] = None

                try:
                    s_acs = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='ACS']]//span[@class='value']").text
                    players.at[_, 's_acs'] = s_acs
                except:
                    players.at[_, 's_acs'] = None

                try:
                    s_kad_ratio = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='KAD Ratio']]//span[@class='value']").text
                    players.at[_, 's_kad_ratio'] = s_kad_ratio
                except:
                    players.at[_, 's_kad_ratio'] = None

                try:
                    s_kills_per_round = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Kills/Round']]//span[@class='value']").text
                    players.at[_, 's_kills_per_round'] = s_kills_per_round
                except:
                    players.at[_, 's_kills_per_round'] = None

                try:
                    s_first_bloods = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='First Bloods']]//span[@class='value']").text
                    players.at[_, 's_first_bloods'] = s_first_bloods
                except:
                    players.at[_, 's_first_bloods'] = None

                try:
                    s_flawless_rounds = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Flawless Rounds']]//span[@class='value']").text
                    players.at[_, 's_flawless_rounds'] = s_flawless_rounds
                except:
                    players.at[_, 's_flawless_rounds'] = None

                try:
                    s_aces = driver.find_element(By.XPATH, "//div[@class='numbers' and .//span[text()='Aces']]//span[@class='value']").text
                    players.at[_, 's_aces'] = s_aces
                except:
                    players.at[_, 's_aces'] = None

                #Randomizing scrape coolwdowns
                time.sleep(uniform(4, 10))
                print(f"Current player: {row['user']}")
                print(players.iloc[[_]].to_string(index=False))
                break

            except WebDriverException as e:
                print(f"WebDriver error: {e}. Sleeping 30 minutes.")
                time.sleep(1800)
        count += 1

#If ctrl+c while running
except KeyboardInterrupt as ki:
    print(f"Keyboard Interrupted, saving valorant_player_stats.csv")

#In any error or issue, save the scraped data
finally:
    players.to_csv('valorant_players_stats_final.csv', index=False)
    driver.quit()
