from pynput import keyboard
from RealtimeTTS import TextToAudioStream, OpenAIEngine, CoquiEngine
from RealtimeSTT import AudioToTextRecorder
from beeps import beep, beeper
from clock import clock
import traceback
import time
import os


# Set '01_PORT' if it's not already set
if '01_PORT' not in os.environ:
    os.environ['01_PORT'] = '10000'
    

if __name__ == '__main__':

    from profiles.default import interpreter

    # Audio setup
    recorder = AudioToTextRecorder()
    recorder.stop()
    
    if interpreter.tts == "coqui":
        engine = CoquiEngine()
    elif interpreter.tts == "openai":
        engine = OpenAIEngine()

    stream = TextToAudioStream(engine)

    # Start clock
    clock()

    # Startup interface
    beep("Blow")
    stream.feed("Hi, how can I help you?")
    stream.play_async()
    print("\n" * 42 + "\nPress and hold 'esc', speak, then release.\n")

    # Remember this, to quit interpreter if pressed again
    last_pressed = 0
    is_pressed = False

    while True:
        try:
            def on_press(key):
                global last_pressed
                global is_pressed

                if key == keyboard.Key.esc and not is_pressed:
                    beep("Morse")
                    is_pressed = True
                    last_pressed = time.time()
                    recorder.start()
                    stream.stop()

            def on_release(key):
                global last_pressed
                global is_pressed

                if key == keyboard.Key.esc and is_pressed:
                    beep("Frog")
                    is_pressed = False
                    recorder.stop()
                    text = recorder.text()
                    print(text)
                    
                    if text.strip() and time.time() - last_pressed > 0.25:
                        
                        def generator():
                            try:
                                global last_pressed
                                old_last_pressed = last_pressed

                                beeper.start()

                                if interpreter.llm.supports_functions == False:
                                    prev_message = None
                                    for message in interpreter.messages:
                                        if message.get("type") == "code":
                                            if prev_message and prev_message.get("role") == "assistant":
                                                prev_message["content"] += "\n```\n" + message.get("content").strip("\n`") + "\n```"
                                            else:
                                                message["type"] = "message"
                                                message["content"] = "```\n" + message.get("content").strip("\n`") + "\n```"
                                        prev_message = message
                                    
                                    interpreter.messages = [message for message in interpreter.messages if message.get("type") != "code"]

                                for chunk in interpreter.chat(text, display=True, stream=True):

                                    if old_last_pressed != last_pressed:
                                        beeper.stop()
                                        break
                                    
                                    if chunk.get("type") == "message":
                                        content = chunk.get("content")
                                        if content:
                                            content = content.replace(". ", ". ... ").replace(", ", ", ... ").replace("!", "! ... ").replace("?", "? ... ")
                                            beeper.stop()
                                            yield content                                             

                                    if "start" in chunk and chunk.get("type") == "code":
                                        beeper.start()
                                
                            except KeyboardInterrupt:
                                raise
                            except:
                                print(traceback.format_exc())

                        stream.feed(generator())
                        stream.play_async()

            while True:
                try:
                    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                        listener.join()
                except KeyboardInterrupt:
                    raise
                except:
                    print(traceback.format_exc())
        except KeyboardInterrupt:
            raise
        except:
            print(traceback.format_exc())