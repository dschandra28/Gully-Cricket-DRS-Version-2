def evaluate_lbw(pitch_x, impact_x, wicket_x, predicted_path, frame_width):
    # Use frame-relative zones instead of fixed pixel values
    leg_boundary = int(frame_width * 0.33)
    off_boundary = int(frame_width * 0.66)

    # Determine zones
    pitch_zone = "In Line" if leg_boundary < pitch_x < off_boundary else "Outside Leg"
    impact_zone = "In Line" if leg_boundary < impact_x < off_boundary else "Outside Off"
    hitting_wickets = leg_boundary < wicket_x < off_boundary

    if pitch_zone == "Outside Leg":
        return "Not Out", pitch_zone, impact_zone, "Missing"
    if impact_zone != "In Line":
        return "Not Out", pitch_zone, impact_zone, "Missing"
    if hitting_wickets:
        return "Out", pitch_zone, impact_zone, "Hitting"
    return "Not Out", pitch_zone, impact_zone, "Missing"
