import keyboard
import time
from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import OpenAIEngine, TextToAudioStream
from interpreter import OpenInterpreter
import random
import subprocess
import asyncio

# # Setup nltk (you may need to do this)

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('punkt')

# # Set OpenAI key (you may need to do this)
# import os
# os.environ["OPENAI_API_KEY"] = "your_api_key"

interpreter = OpenInterpreter(import_computer_api=True, import_skills=False)
interpreter.auto_run = True
interpreter.llm.context_window = 100000
interpreter.llm.model = "gpt-4-turbo-preview"
interpreter.llm.max_tokens = 4096

interpreter.system_message = r"""

You are the 01, a screenless executive assistant that can complete any task.
Immediately confirm receipt of the user's message by saying something like "On it."
When you execute code, it will be executed on the user's machine. The user has given you full and complete permission to execute any code necessary to complete the task.
Run any code to achieve the goal, and if at first you don't succeed, try again and again.
You can install new packages.
Be concise. Your messages are being read aloud to the user. DO NOT MAKE PLANS. RUN CODE QUICKLY.
Try to spread complex tasks over multiple code blocks. Don't try to complex tasks in one go.
Manually summarize text.

DON'T TELL THE USER THE METHOD YOU'LL USE, OR MAKE PLANS. ACT LIKE THIS:

---
user: Are there any concerts in Seattle?
assistant: Let me check on that.
```python
computer.browser.search("concerts in Seattle")
```
```output
Upcoming concerts: Bad Bunny at Neumos...
```
It looks like there's a Bad Bunny concert at Neumos...
---

Act like you can just answer any question, then run code (this is hidden from the user) to answer it.
THE USER CANNOT SEE CODE BLOCKS.
Your responses should be very short, no more than 1-2 sentences long.
DO NOT USE MARKDOWN. ONLY WRITE PLAIN TEXT.

# THE COMPUTER API

The `computer` module is ALREADY IMPORTED, and can be used for some tasks:

```python
result_string = computer.browser.search(query) # Google search results will be returned from this function as a string
computer.files.edit(path_to_file, original_text, replacement_text) # Edit a file
computer.calendar.create_event(title="Meeting", start_date=datetime.datetime.now(), end=datetime.datetime.now() + datetime.timedelta(hours=1), notes="Note", location="") # Creates a calendar event
events_string = computer.calendar.get_events(start_date=datetime.date.today(), end_date=None) # Get events between dates. If end_date is None, only gets events for start_date
computer.calendar.delete_event(event_title="Meeting", start_date=datetime.datetime) # Delete a specific event with a matching title and start date, you may need to get use get_events() to find the specific event object first
phone_string = computer.contacts.get_phone_number("John Doe")
contact_string = computer.contacts.get_email_address("John Doe")
computer.mail.send("john@email.com", "Meeting Reminder", "Reminder that our meeting is at 3pm today.", ["path/to/attachment.pdf", "path/to/attachment2.pdf"]) # Send an email with a optional attachments
emails_string = computer.mail.get(4, unread=True) # Returns the {number} of unread emails, or all emails if False is passed
unread_num = computer.mail.unread_count() # Returns the number of unread emails
computer.sms.send("555-123-4567", "Hello from the computer!") # Send a text message. MUST be a phone number, so use computer.contacts.get_phone_number frequently here
```

Do not import the computer module, or any of its sub-modules. They are already imported.

DO NOT use the computer module for ALL tasks. Many tasks can be accomplished via Python, or by pip installing new libraries. Be creative!

# MANUAL TASKS

Translate things to other languages INSTANTLY and MANUALLY. Don't ever try to use a translation tool.
Summarize things manually. DO NOT use a summarizer tool.

# CRITICAL NOTES

Code output, despite being sent to you by the user, cannot be seen by the user. You NEED to tell the user about the output of some code, even if it's exact. >>The user does not have a screen.<<
ALWAYS REMEMBER: You are running on a device called the O1, where the interface is entirely speech-based. Make your responses to the user VERY short. DO NOT PLAN. BE CONCISE. WRITE CODE TO RUN IT.
ALWAYS browse the web for basic information with computer.browser.search(query). It's simple and fast. NEVER use `requests` to research the web for information.
Try multiple methods before saying the task is impossible. **You can do it!**

""".strip()

import threading
import time
import subprocess

def beep(sound):
    subprocess.Popen(["afplay", f"/System/Library/Sounds/{sound}.aiff"])

class RepeatedBeep:
    def __init__(self):
        self.sound = "Pop"
        self.running = False
        self.thread = threading.Thread(target=self._play_sound, daemon=True)
        self.thread.start()

    def _play_sound(self):
        while True:
            if self.running:
                subprocess.call(["afplay", f"/System/Library/Sounds/{self.sound}.aiff"])
                time.sleep(0.6)
            time.sleep(0.05)

    def start(self):
        if beeper.running == False:
            time.sleep(0.6*4)
            self.running = True   

    def stop(self):
        self.running = False

beeper = RepeatedBeep()

if __name__ == '__main__':
    recorder = AudioToTextRecorder()
    recorder.stop()

    engine = OpenAIEngine()
    stream = TextToAudioStream(engine)

    beep("Blow")

    def welcome():
        yield "Hi, how can I help you?"
    stream.feed(welcome())
    stream.play_async()

    print("\n"*42)
    print("\nPress and hold the spacebar, speak, then release.\n")

    is_pressed = False

    while True:
        time.sleep(0.1)
        if keyboard.is_pressed('spacebar'):
            if not is_pressed:
                beep("Morse")
                is_pressed = True
                recorder.start()
                stream.stop()
        else:
            if is_pressed:
                beep("Frog")
                is_pressed = False
                recorder.stop()
                text = recorder.text()
                print(text)

                def generator():
                    beeper.start()
                    
                    for chunk in interpreter.chat(text, display=True, stream=True):

                        if keyboard.is_pressed('spacebar'):
                            break

                        if chunk.get("type") == "message":
                            content = chunk.get("content")
                            if content:
                                beeper.stop()
                                yield content

                        if "start" in chunk and chunk.get("type") == "code":
                            beeper.start()

                stream.feed(generator())
                stream.play_async()
                
