# Get events
# Then get sessions
# then get telemetry data per drive
# then write t0 file
import os
import fastf1

from models.driver_race_data import DriverRaceData
from storage_service import StorageService

def main():
    # TODO: Sanitize input 
    event = input("What event do you want to catalogue? ")
    first_year = input("Starting year? ")
    last_year = input("Ending year? ")

    event_name_no_space = event.replace(" ", "")

    print(f"Retrieving events for: {event} from {first_year} to {last_year}")
    events = retrieve_events(event, int(first_year), int(last_year), event_name_no_space)
    storage_service = StorageService()
    for event in events:
        event_year = event.year
        drivers_data = get_driver_telemetry_data(event)

        storage_service.save_file(f"data/{event_name_no_space}", f"{event_year}.txt", drivers_data)

    storage_service.zip_data_dir()

def retrieve_events(name, first_year, last_year, event_name_no_space):
    events = []
    for i in range(first_year, last_year + 1):
        file_name = f"data/{event_name_no_space}/{i}.txt"
        if os.path.exists(file_name):
            print(f"File {file_name} already exists, skipping...")
            continue
        try:
            events.append(fastf1.get_event(i, name))
        except:
            print(f"Error retrieving event {name} for year: {i}")
    
    return events


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


    drivers_race_data = []
    p1_telemetry = None
    p2_telemetry = None
    p3_telemetry = None

    for i in range(0, len(driver_names)):
        try:
            driver_number = driver_numbers[i]
            driver_name = driver_names[i]
            
            if practice_session_1 != None:
                try:
                    p1_telemetry = practice_session_1.car_data[driver_number]
                except:
                    p1_telemetry = None
                    print(f"No p1 telemetry data for driver: {driver_name}")
            if practice_session_2 != None:
                try:
                    p2_telemetry = practice_session_2.car_data[driver_number]
                except:
                    p2_telemetry = None
                    print(f"No p2 telemetry data for driver: {driver_name}")
            if practice_session_3 != None:
                try:
                    p3_telemetry = practice_session_3.car_data[driver_number]
                except:
                    p3_telemetry = None
                    print(f"No p3 telemetry data for driver: {driver_name}")
    
            q_telemetry = qual_session.car_data[driver_number]
            r_telemetry = race_session.car_data[driver_number]

            drivers_race_data.append(
                DriverRaceData(driver_name, p1_telemetry, p2_telemetry, p3_telemetry, q_telemetry, r_telemetry))
        except Exception as e:
            print(f"ERROR, could not retrieve all tele data for event: {event_name}")

    return drivers_race_data
main()