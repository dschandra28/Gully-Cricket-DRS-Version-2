import gradio as gr
import cv2
import numpy as np
from ball_tracker import detect_ball
from trajectory import predict_trajectory
from lbw_engine import evaluate_lbw
from overlay_display import draw_overlay
import tempfile

def process_video(video_file):
    cap = cv2.VideoCapture(video_file)
    ball_path = []
    output_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        ball = detect_ball(frame)
        if ball:
            ball_path.append(ball)

        if len(ball_path) > 5:
            try:
                a, b, c = predict_trajectory(ball_path)
                trajectory_func = lambda x: a * x**2 + b * x + c
                pitch_x = ball_path[0][0]
                impact_x = ball_path[-1][0]
                wicket_x = int((impact_x + 100) / 2)
                frame_width = frame.shape[1]
                verdict, pitch, impact, wickets = evaluate_lbw(pitch_x, impact_x, wicket_x, ball_path, frame_width)
                frame = draw_overlay(frame, ball_path, trajectory_func, verdict, (pitch, impact, wickets))
            except Exception as e:
                print("Prediction error:", e)

        output_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()

    return output_frames[-1] if output_frames else None


demo = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Upload a Cricket Delivery Video"),
    outputs=gr.Image(label="Decision Frame with Overlay"),
    title="🏏 Gully Cricket DRS - LBW Analysis"
)

if __name__ == "__main__":
    demo.launch(inbrowser=True, share=False)

