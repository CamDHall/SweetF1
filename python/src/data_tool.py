from models.session_telemetry_data import RacePositionData, SessionTelemetryData


def extract_data(session_data, driver_number):
    telemetry = session_data.car_data[driver_number]
    try:
        telemetry = telemetry.interpolate()
        positions_raw = session_data.pos_data[driver_number]

        positions = []

        for i in range(len(positions_raw) - 1):
            position = RacePositionData(
                x=positions_raw['X'].values[i],
                y=positions_raw['Y'].values[i],
                z=positions_raw['Z'].values[i]
            )

            positions.append(position)

        telemetry_obj = SessionTelemetryData(
            positions=positions,
            speeds=telemetry['Speed'].values.tolist(),
            rpms=telemetry['RPM'].values.tolist(),
            gears=telemetry['nGear'].values.tolist(),
            brakes=telemetry['Brake'].values.tolist(),
            throttles=telemetry['Throttle'].values.tolist(),
            drs=telemetry['DRS'].values.tolist()
        )

        return telemetry_obj
    except Exception as e:
        print(f"Error interpolating telemetry data: {e}")
        return None
