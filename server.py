from pynput import keyboard
from RealtimeTTS import TextToAudioStream, OpenAIEngine, CoquiEngine
from RealtimeSTT import AudioToTextRecorder
from beeps import beep, beeper
from clock import clock
import traceback
import time
import os
from pynput.keyboard import Controller

controller = Controller()

# These callbacks will contain the audio chunks for STT and TTS
def on_stt_chunk(chunk):
    return
    print(chunk)
def on_tts_chunk(chunk):
    return
    print(str(chunk)[:1])

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
    #clock()

    # Startup interface
    beep("Blow")
    stream.feed("Hi, how can I help you?")
    stream.play_async(on_audio_chunk=on_tts_chunk, muted=False) # This is TTS. Muted should be True, once we figure out how to use on_tts_chunk to send the chunk over the server to the client, and play it there.
    print("\n" * 42 + "\nPress and hold 'esc', speak, then release.\n")
    wake_key = keyboard.Key.ctrl

    # Button state
    last_pressed = 0
    is_pressed = False

    while True:
        try:
            def on_press(key):
                global last_pressed
                global is_pressed

                if key == wake_key and not is_pressed:
                    beep("Morse")
                    is_pressed = True
                    last_pressed = time.time()
                    recorder.start()
                    stream.stop()

            def on_release(key):
                global last_pressed
                global is_pressed

                if key == wake_key and is_pressed:
                    beep("Frog")
                    is_pressed = False
                    recorder.stop()
                    text = recorder.text()
                    print(text)
                    
                    if text.strip() and time.time() - last_pressed > 0.25:
                        
                        def generator(text):
                            try:
                                global last_pressed
                                old_last_pressed = last_pressed

                                beeper.start()

                                # Experimental: This helps Groq sometimes. I maybe it should be in OI.
                                # if interpreter.llm.supports_functions == False:
                                #     prev_message = None
                                #     for message in interpreter.messages:
                                #         if message.get("type") == "code":
                                #             if prev_message and prev_message.get("role") == "assistant":
                                #                 prev_message["content"] += "\n```\n" + message.get("content").strip("\n`") + "\n```"
                                #             else:
                                #                 message["type"] = "message"
                                #                 message["content"] = "```\n" + message.get("content").strip("\n`") + "\n```"
                                #         prev_message = message
                                    
                                #     interpreter.messages = [message for message in interpreter.messages if message.get("type") != "code"]

                                # text = text + "\n\n" + interpreter.computer.os.get_selected_text() + "\n\nOnly send the modified text. Don't send anything else!"
                                # interpreter.messages = []
                                
                                for chunk in interpreter.chat(text, display=True, stream=True):

                                    if old_last_pressed != last_pressed:
                                        beeper.stop()
                                        break

                                    content = chunk.get("content")
                                    
                                    if chunk.get("type") == "message":

                                        if content:
                                            beeper.stop()
                                            
                                            # Experimental: The AI voice sounds better with replacements like these, but it should happen at the TTS layer
                                            # content = content.replace(". ", ". ... ").replace(", ", ", ... ").replace("!", "! ... ").replace("?", "? ... ")

                                            yield content

                                    elif chunk.get("type") == "code":
                                        if "start" in chunk:
                                            beeper.start()

                                        # Experimental: If the AI wants to type, we should type immediatly
                                        if interpreter.messages[-1].get("content").startswith("computer.keyboard.write("):
                                            controller.type(content)
                                        
                                
                            except KeyboardInterrupt:
                                raise
                            except:
                                print(traceback.format_exc())

                        stream.feed(generator(text))
                        stream.play_async(on_audio_chunk=on_tts_chunk, muted=False) # This is TTS. Muted should be True, once we figure out how to use on_tts_chunk to send the chunk over the server to the client, and play it there.

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