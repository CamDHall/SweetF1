# Get events
# Then get sessions
# then get telemetry data per drive
# then write t0 file
from dataclasses import asdict
import os
import fastf1

from models.driver_race_data import DriverRaceData, SessionName
from data_tool import extract_data
from storage_service import StorageService

storage_service = StorageService()

def main():
    # TODO: Sanitize input 
    event = "French Grand Prix"
    first_year = "2022"
    last_year = "2022"
    race_data_only = True
    #event = input("What event do you want to catalogue? ")
    #first_year = input("Starting year? ")
    #last_year = input("Ending year? ")
    #race_data_only_input = input("Only retrieve race data? (y/n) ")
    #race_data_only = race_data_only_input.lower() == "y"

    event_name_no_space = event.replace(" ", "")

    print(f"Retrieving events for: {event} from {first_year} to {last_year}")
    events = retrieve_events(event, int(first_year), int(last_year), event_name_no_space)
    for event in events:
        get_driver_telemetry_data(event)

def retrieve_events(name, first_year, last_year, event_name_no_space):
    events = []
    for i in range(first_year, last_year + 1):
        file_name = f"data/{event_name_no_space}/{i}.json"
        if os.path.exists(file_name):
            print(f"File {file_name} already exists, skipping...")
            continue
        try:
            events.append(fastf1.get_event(i, name))
        except:
            print(f"Error retrieving event {name} for year: {i}")
    
    return events

def save_session_data(event_name, event_year, driver_name, session_name, telemetry_data):
    data = DriverRaceData(driver_name, session_name, telemetry_data)
    storage_service.save_file(f"data/{event_name}/{event_year}/{driver_name}", f"{session_name.name}.json", asdict(data))

def get_driver_telemetry_data(event):
    event_year = event.year
    event_name = event["EventName"]

    # Not all events have all sessions
    practice_session_1 = None
    practice_session_2 = None
    practice_session_3 = None
    try:
        practice_session_1 = fastf1.get_session(event_year, event_name, "fp1")
    except:
        print(f"Missing p1 session for event: {event_name}")
    try:
        practice_session_2 =  fastf1.get_session(event_year, event_name, "fp2")
    except:
        print(f"Missing p2 session for event: {event_name}")
    try:
        practice_session_3 =  fastf1.get_session(event_year, event_name, "fp3")
    except:
        print(f"Missing p3 session for {event_name}")
        
    qual_session =  fastf1.get_session(event_year, event_name, "q")
    race_session =  fastf1.get_session(event_year, event_name, "r")

    if practice_session_1 != None:
        practice_session_1.load()
        practice_session_1._load_telemetry()
    if practice_session_2 != None:
        practice_session_2.load()
        practice_session_2._load_telemetry()
    if practice_session_3 != None:
        practice_session_3.load()
        practice_session_3._load_telemetry()

    qual_session.load()
    qual_session._load_telemetry()
    race_session.load()
    race_session._load_telemetry()

    driver_names = race_session.results["FullName"].values
    driver_numbers = race_session.results["DriverNumber"].values

    for i in range(0, len(driver_names)):
        try:
            driver_number = driver_numbers[i]
            driver_name = driver_names[i]
            
            if practice_session_1 != None:
                try:
                    save_session_data(event_name, event_year, driver_name, SessionName.P_1, 
                                      extract_data(practice_session_1, driver_number))
                except:
                    print(f"No p1 telemetry data for driver: {driver_name}")
            if practice_session_2 != None:
                try:
                    save_session_data(event_name, event_year, driver_name, SessionName.P_2, 
                                      extract_data(practice_session_2, driver_number))
                except:
                    print(f"No p2 telemetry data for driver: {driver_name}")
            if practice_session_3 != None:
                try:
                    save_session_data(event_name, event_year, driver_name, SessionName.P_3, 
                                      extract_data(practice_session_3, driver_number))
                except:
                    print(f"No p3 telemetry data for driver: {driver_name}")

            save_session_data(event_name, event_year, driver_name, SessionName.Q, extract_data(qual_session, driver_number))
            save_session_data(event_name, event_year, driver_name, SessionName.R, extract_data(race_session, driver_number))

        except Exception as e:
            print(f"ERROR, could not retrieve all tele data for event: {event_name}")

main()