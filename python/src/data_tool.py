from models.session_telemetry_data import RacePositionData, SessionTelemetryData


def extract_data(session_data, driver_number):
    p1_telemetry = session_data.car_data[driver_number]
    try:
        p1_telemetry = p1_telemetry.interpolate()
        s = p1_telemetry['Speed'].values.tolist()
        rpm = p1_telemetry['RPM'].values.tolist()
        gear = p1_telemetry['nGear'].values.tolist()
        brake = p1_telemetry['Brake'].values.tolist()
        throttle = p1_telemetry['Throttle'].values.tolist()
        drs = p1_telemetry['DRS'].values.tolist()
        position = session_data.pos_data[driver_number]
        pos_date = position['Date'].values.tolist()
        pos_time = position['Time'].values.tolist()
        pos_x = position['X'].values.tolist()
        pos_y = position['Y'].values.tolist()
        pos_z = position['Z'].values.tolist()

        position_obj = RacePositionData(
            date=pos_date,
            time=pos_time,
            x=pos_x,
            y=pos_y,
            z=pos_z
        )

        telemetry_obj = SessionTelemetryData(
            position=position_obj,
            speed=s,
            rpm=rpm,
            gear=gear,
            brake=brake,
            throttle=throttle,
            drs=drs
        )

        return telemetry_obj
    except Exception as e:
        print(f"Error interpolating telemetry data: {e}")
        return None
