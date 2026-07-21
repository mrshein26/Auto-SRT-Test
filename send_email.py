import os
import smtplib
from email.message import EmailMessage

# GitHub Secrets မှ အချက်အလက်များ ရယူခြင်း
sender_email = os.environ.get("EMAIL_ADDRESS")
sender_password = os.environ.get("EMAIL_PASSWORD")
recipient_email = os.environ.get("RECIPIENT_EMAIL")

# အီးမေးလ် အကြောင်းအရာများ ရေးသားခြင်း
msg = EmailMessage()
msg['Subject'] = 'သင့်၏ စာတန်းထိုး (SRT) ဖိုင် ရရှိပါပြီ'
msg['From'] = sender_email
msg['To'] = recipient_email
msg.set_content('GitHub Actions (Whisper AI) မှ အလိုအလျောက် ထုတ်ယူထားသော SRT ဖိုင်ကို ပူးတွဲ ပေးပို့အပ်ပါသည်။')

# ထွက်လာမည့် audio.srt ဖိုင်ကို အီးမေးလ်တွင် ပူးတွဲထည့်သွင်းခြင်း
try:
    with open("audio.srt", 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='subtitle.srt')
except FileNotFoundError:
    print("SRT ဖိုင် ရှာမတွေ့ပါ။ AI ထုတ်ယူခြင်း အဆင့်တွင် အမှားအယွင်း ရှိနိုင်ပါသည်။")
    exit(1)

# Gmail ဆာဗာမှ တဆင့် ပေးပို့ခြင်း
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    print("အီးမေးလ် အောင်မြင်စွာ ပို့ပြီးပါပြီ!")
except Exception as e:
    print(f"အီးမေးလ် ပို့ရာတွင် အမှားအယွင်းဖြစ်နေပါသည် - {e}")
