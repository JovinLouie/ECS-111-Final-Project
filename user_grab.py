import pandas as pd
import requests
import os, time
from ratelimit import limits, sleep_and_retry
from valo_api import set_api_key
from valo_api.endpoints import (
    get_match_history_by_puuid_v3,
    get_raw_match_details_data_v1,
    get_account_details_by_name_v2
)

#30 calls, for each minute
CALLS = 30
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def safe_get_match_history(puuid):
    return get_match_history_by_puuid_v3(region="na", puuid=puuid)

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def safe_get_account(name, tag):
    return get_account_details_by_name_v2(name, tag, True)

#First player to grab
def initial_user_grab(name, tag):
    info = safe_get_account(name, tag)
    return info.puuid

#Recursive function
def grab_info(puuid, dataframe, seen_puuids):
    if len(dataframe) >= 800 or puuid in seen_puuids:
        return dataframe, seen_puuids

    #Sleeping to respect call spamming
    time.sleep(10)

    try:
        print(f"Fetching match history for: {puuid}")
        matches = safe_get_match_history(puuid)
        seen_puuids.add(puuid)

        if not matches:
            return dataframe, seen_puuids

        match = matches[0]
        #Grab all players in the player's lobby, if they aren't already in the dataframe
        for player in match.players.all_players:
            player_puuid = player.puuid
            player_name = player.name
            player_tag = player.tag

            if player_puuid not in dataframe['puuid'].values:
                print(f"   + Adding {player_name}#{player_tag}")
                dataframe = pd.concat([dataframe, pd.DataFrame([{
                    'puuid': player_puuid,
                    'user': player_name,
                    'tag': player_tag
                }])], ignore_index=True)

        # Recursively grab next match group
        for player in match.players.all_players:
            #If dataframe hits limit, finish recursion
            if len(dataframe) >= 800:
                break
            #Otherwise, with the seen_puuids and current dataframe, take the next player in the match
            dataframe, seen_puuids = grab_info(player.puuid, dataframe, seen_puuids)

    except Exception as e:
        print(f"⚠️ Error for puuid {puuid}: {e}")
        time.sleep(60)
    
    return dataframe, seen_puuids

def main():
    set_api_key("HDEV-6008a938-6d58-4cac-8fdf-8312351d06c9")  # Replace with your key if needed (this key is expired)

    # Starting point
    storage = pd.DataFrame(columns=['puuid', 'user', 'tag'])
    seen_puuids = set()

    starting_puuid = initial_user_grab("donkdonktime", "donk")
    storage, seen_puuids = grab_info(starting_puuid, storage, seen_puuids)

    # Done
    print("\nFinished grabbing users.")
    print(storage)
    storage.to_csv("valorant_players.csv", index=False)

if __name__ == "__main__":
    main()
