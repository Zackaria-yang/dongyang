from mydetect import *
import cv2
from pic2video import pic2video

segmodel = Segmodel(cuda=False, weights='logs/b0_100/weights/best_epoch_weights.pth', mix_type=2)
segmodel.init_model()

video_file_name = "video/干扰3.mp4"
vc = cv2.VideoCapture(video_file_name)
if vc.isOpened():
    ret, frame = vc.read()
else:
    ret = False

count = 0  # 记录图片个数
frame_interval = 1
frame_interval_count = 0

while ret:
    ret, frame = vc.read()
    if frame is None or ret is None:
        break
    if frame_interval_count % frame_interval == 0:
        # fps_pic = "video/video_fps/" + str(count) + ".png"
        cv2.imwrite("1.png", frame)
        seg_result = segmodel.detect("1.png")
        seg_result = cv2.cvtColor(seg_result, cv2.COLOR_BGR2RGB)
        # cv2.imshow("pic",seg_result)
        # cv2.waitKey(0)
        pic_name = "video/video_pic/" + str(count) + ".png"
        cv2.imwrite(pic_name, seg_result)
        count += 1
    frame_interval_count += 1

print("count:", count)
print("frame_interval:", frame_interval)
print("frame_interval_count:", frame_interval_count)

vc.release()

pic2video(r'video/video_pic', (640, 480))
