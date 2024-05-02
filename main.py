from profiles.default import interpreter
from pynput import keyboard
from RealtimeTTS import TextToAudioStream, OpenAIEngine, CoquiEngine
from RealtimeSTT import AudioToTextRecorder
from beeps import beep, beeper
import time

if __name__ == '__main__':
    recorder = AudioToTextRecorder()
    recorder.stop()
    
    if interpreter.tts == "coqui":
        engine = CoquiEngine()
    elif interpreter.tts == "openai":
        engine = OpenAIEngine()

    stream = TextToAudioStream(engine)

    beep("Blow")

    stream.feed("Hi, how can I help you?")
    stream.play_async()

    print("\n" * 42)
    print("\nPress and hold 'esc', speak, then release.\n")

    is_pressed = False
    language_model_on = False
    last_pressed = 0
    wildcard_index = 0

    ## CODE GETS MESSY.

    while True:
        try:
            def on_press(key):
                global is_pressed
                global last_pressed
                global wildcard_index
                global language_model_on
                if language_model_on:
                    return
                try:
                    if key == keyboard.Key.esc and not is_pressed:
                        beep("Morse")
                        last_pressed = time.time()
                        is_pressed = True
                        recorder.start()
                        stream.stop()
                    
                except AttributeError:
                    pass

            def on_release(key):
                global is_pressed
                global last_pressed
                global language_model_on
                if language_model_on:
                    return

                try:
                    if key == keyboard.Key.esc and is_pressed:
                        beep("Frog")
                        is_pressed = False
                        recorder.stop()
                        text = recorder.text()
                        print(text)
                        
                        if text.strip() and time.time() - last_pressed > 0.5:
                            
                            def generator():
                                try:
                                    global last_pressed
                                    global language_model_on

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

                                    language_model_on = True
                                    for chunk in interpreter.chat(text, display=True, stream=True):
                                        # if old_last_pressed != last_pressed:
                                        #     beeper.stop()
                                        #     print("BREAKING!")
                                        #     break
                                        
                                        if chunk.get("type") == "message":
                                            content = chunk.get("content")
                                            if content:
                                                #content = content.replace(". ", ". ... ").replace(", ", ", ... ").replace("!", "! ... ").replace("?", "? ... ")
                                                beeper.stop()
                                                yield content                                             

                                        if "start" in chunk and chunk.get("type") == "code":
                                            beeper.start()

                                    language_model_on = False   
                                    
                                except Exception as e:
                                    print(str(e))


                            stream.feed(generator())
                            
                            stream.play_async()
                        
                        
                except AttributeError:
                    pass

            while True:
                try:
                    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                        listener.join()
                except Exception as e:
                    print(f"An error occurred: {e}. Retrying...")
        except Exception as e:
            print(str(e))