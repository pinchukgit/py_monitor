import ffmpeg
import os
import datetime
import settings

video_path = os.path.join(settings.BASE_DIR, 'video')
users = os.listdir(settings.SCREEN_DIR)

current_date = datetime.datetime.now() + datetime.timedelta(days=1)

for user in users:
    prev_day = current_date - datetime.timedelta(days=1)
    date_dir = prev_day.strftime("%Y/%-m/%-d")

    path = os.path.join(settings.SCREEN_DIR, f"{user}/{date_dir}")
    if os.path.exists(path):
        input = ffmpeg.input(os.path.join(path, "*.png"), pattern_type='glob',
                             framerate=2)
        output_dir = os.path.join(video_path, user)
        os.makedirs(output_dir, exist_ok=True)
        input.output(
            os.path.join(output_dir,
                         prev_day.strftime("%Y-%m-%d.mp4")),
            pix_fmt="yuv420p").global_args('-n').run()
