import cv2
from ball_tracker import detect_ball
from trajectory import predict_trajectory
from lbw_engine import evaluate_lbw
from overlay_display import draw_overlay

cap = cv2.VideoCapture(0)
ball_path = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    ball = detect_ball(frame)
    if ball:
        ball_path.append(ball)

    if len(ball_path) > 5:
        a, b, c = predict_trajectory(ball_path)
        trajectory_func = lambda x: a * x**2 + b * x + c

        pitch_x = ball_path[0][0]
        impact_x = ball_path[-1][0]
        wicket_x = int((impact_x + 100) / 2)

        verdict, pitch, impact, wickets = evaluate_lbw(pitch_x, impact_x, wicket_x, ball_path)
        frame = draw_overlay(frame, ball_path, trajectory_func, verdict, (pitch, impact, wickets))

    cv2.imshow("Gully Cricket DRS", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
