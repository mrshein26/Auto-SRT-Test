import cv2
import pytesseract
from datetime import timedelta

def format_time(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def extract_subtitles(video_path, srt_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # ၁ စက္ကန့်လျှင် ၁ ပုံနှုန်းဖြင့်သာ စစ်ဆေးရန် (မြန်ဆန်စေရန်)
    frame_interval = int(fps) 
    
    srt_file = open(srt_path, 'w', encoding='utf-8')
    
    frame_count = 0
    sub_index = 1
    previous_text = ""
    start_time = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # သတ်မှတ်ထားသော Frame ရောက်တိုင်းသာ စစ်ဆေးမည်
        if frame_count % frame_interval == 0:
            current_seconds = frame_count / fps
            
            # ဗီဒီယို၏ အောက်ခြေ (စာတန်းထိုးရှိတတ်သော နေရာ) ကို ဖြတ်ယူခြင်း
            height, width, _ = frame.shape
            cropped_frame = frame[int(height*0.75):height, 0:width]
            
            # စာဖတ်ရလွယ်ကူစေရန် အဖြူအမည်း (Grayscale) ပြောင်းခြင်း
            gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            
            # မြန်မာဘာသာ (mya) ဖြင့် OCR ဖတ်ခြင်း
            text = pytesseract.image_to_string(thresh, lang='mya').strip()
            
            if text and text != previous_text:
                end_time = current_seconds
                if previous_text:
                    # ယခင်စာသားကို SRT အဖြစ် ရေးသားခြင်း
                    srt_file.write(f"{sub_index}\n")
                    srt_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                    srt_file.write(f"{previous_text}\n\n")
                    sub_index += 1
                
                previous_text = text
                start_time = current_seconds
                
        frame_count += 1

    # နောက်ဆုံးကျန်ရှိနေသော စာသားကို ရေးရန်
    if previous_text:
        srt_file.write(f"{sub_index}\n")
        srt_file.write(f"{format_time(start_time)} --> {format_time(start_time + 2)}\n")
        srt_file.write(f"{previous_text}\n\n")

    srt_file.close()
    cap.release()
    print("OCR ဖြင့် မြန်မာစာတမ်းထိုး ထုတ်ယူခြင်း ပြီးဆုံးပါပြီ။")

# Code စတင် အလုပ်လုပ်မည့်နေရာ
extract_subtitles('video.mp4', 'audio.srt')
