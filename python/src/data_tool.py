from models.session_telemetry_data import RacePositionData, SessionTelemetryData


def extract_data(session_data, driver_number):
    p1_telemetry = session_data.car_data[driver_number]
    try:
        p1_telemetry = p1_telemetry.interpolate()
        position = session_data.pos_data[driver_number]

        position_obj = RacePositionData(
            date=position['Date'].values.tolist(),
            time=position['Time'].values.tolist(),
            x=position['X'].values.tolist(),
            y=position['Y'].values.tolist(),
            z=position['Z'].values.tolist()
        )

        telemetry_obj = SessionTelemetryData(
            position=position_obj,
            speed=p1_telemetry['Speed'].values.tolist(),
            rpm=p1_telemetry['RPM'].values.tolist(),
            gear=p1_telemetry['nGear'].values.tolist(),
            brake=p1_telemetry['Brake'].values.tolist(),
            throttle=p1_telemetry['Throttle'].values.tolist(),
            drs=p1_telemetry['DRS'].values.tolist()
        )

        return telemetry_obj
    except Exception as e:
        print(f"Error interpolating telemetry data: {e}")
        return None
