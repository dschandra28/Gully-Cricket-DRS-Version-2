import cv2

def draw_overlay(frame, ball_points, trajectory_func, verdict, labels):
    height, width = frame.shape[:2]

    # 1. Draw smooth RED arc (trajectory)
    draw_trajectory_arc(frame, trajectory_func, ball_points[0][0], ball_points[-1][0])

    # 2. Draw BLUE prediction line from impact point forward
    if len(ball_points) > 1:
        draw_prediction_line(frame, ball_points[-1], trajectory_func)

    # 3. Draw YELLOW stumps (centered)
    draw_stumps(frame, width // 2)

    # 4. Display Decision and Details
    text_color = (0, 255, 0) if verdict == "Out" else (0, 255, 255)
    cv2.putText(frame, f"Decision: {verdict}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, text_color, 3)
    cv2.putText(frame, f"Pitching: {labels[0]}", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.putText(frame, f"Impact: {labels[1]}", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.putText(frame, f"Wickets: {labels[2]}", (20, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    return frame


# ============================
# 📦 Helper Drawing Functions
# ============================

def draw_trajectory_arc(frame, trajectory_func, start_x, end_x, step=5, color=(0, 0, 255)):
    height, width = frame.shape[:2]
    for x in range(start_x, min(end_x, width - step), step):
        try:
            y1 = int(trajectory_func(x))
            y2 = int(trajectory_func(x + step))
            if 0 <= y1 < height and 0 <= y2 < height:
                cv2.line(frame, (x, y1), (x + step, y2), color, 2)
        except:
            continue

def draw_prediction_line(frame, start_point, trajectory_func, distance=100, color=(255, 0, 0)):
    x1 = start_point[0]
    x2 = x1 + distance
    try:
        y2 = int(trajectory_func(x2))
        height, width = frame.shape[:2]
        if 0 <= y2 < height and x2 < width:
            cv2.line(frame, start_point, (x2, y2), color, 2)
    except:
        pass

def draw_stumps(frame, center_x, color=(0, 255, 255)):
    height = frame.shape[0]
    stump_top = int(height * 0.55)
    stump_bottom = int(height * 0.85)
    for dx in [-10, 0, 10]:
        cv2.line(frame, (center_x + dx, stump_top), (center_x + dx, stump_bottom), color, 2)

def draw_ball_path(frame, ball_path, color=(0, 255, 0)):
    for i in range(1, len(ball_path)):
        cv2.line(frame, ball_path[i - 1], ball_path[i], color, thickness=2)

def draw_ball(frame, position, radius=5, color=(0, 0, 255)):
    cv2.circle(frame, position, radius, color, -1)

def draw_pitch_impact_wickets(frame, pitch, impact, wickets):
    cv2.putText(frame, f"Pitch: {pitch}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.putText(frame, f"Impact: {impact}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.putText(frame, f"Wickets: {wickets}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
