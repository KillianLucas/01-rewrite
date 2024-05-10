####################
# Experimental.
####################

from interpreter import interpreter

# This is an Open Interpreter compatible profile.
# Visit https://01.openinterpreter.com/profile for all options.


# Connect your 01 to a language model
interpreter.llm.model = "gpt-4-turbo"
interpreter.llm.context_window = 100000
interpreter.llm.max_tokens = 4096
#interpreter.llm.api_key = "<your_openai_api_key_here>"

# Give your 01 a voice
interpreter.tts = "openai"

# Tell your 01 where to find and save skills
interpreter.computer.skills.path = "./skills"

# Extra settings
interpreter.computer.import_computer_api = True
interpreter.computer.import_skills = True
interpreter.computer.run("python", "computer") # This will trigger those imports
interpreter.auto_run = True
interpreter.loop = True
interpreter.loop_message = """Proceed with what you were doing (this is not confirmation, if you just asked me something). You CAN run code on my machine. If you want to run code, start your message with "```"! If the entire task is done, say exactly 'The task is done.' If you need some specific information (like username, message text, skill name, skill step, etc.) say EXACTLY 'Please provide more information.' If it's impossible, say 'The task is impossible.' (If I haven't provided a task, say exactly 'Let me know what you'd like to do next.') Otherwise keep going. CRITICAL: REMEMBER TO FOLLOW ALL PREVIOUS INSTRUCTIONS. If I'm teaching you something, remember to run the related `computer.skills.new_skill` function."""
interpreter.loop_breakers = [
    "The task is done.",
    "The task is impossible.",
    "Let me know what you'd like to do next.",
    "Please provide additional information.",
]

interpreter.force_task_completion_message = "PLEASE ENSURE YOU RUN COMPUTER.KEYBOARD.WRITE IF YOU HAVEN'T ALREADY. Just do it once though. If you have, say 'The task is done.' exactly."
interpreter.force_task_completion_breakers = [
    "The task is done.",
    "The task is impossible.",
    "Let me know what you'd like to do next.",
    "Please provide more information.",
]

# Set the identity and personality of your 01
interpreter.system_message = '''

The user has selected the following text at this moment, and will ask you to modify it:

"""
{{computer.os.get_selected_text()}}
"""

Please run `text = computer.os.get_selected_text()` to get the original text, then fulfill the user's request by typing the modified text with `computer.keyboard.write(new_text)`, acting like this:
You also have access to a browser— `computer.browser.search(query)`. Use this to perform research.
Don't do everything programatically. Sometimes you will just type out changes manually. Sometimes you will combine programatic and manual solutions.

User: Make this uppercase.
You: Making the text uppercase.
```
text = computer.os.get_selected_text() # I use this to programatically get the selected text.
computer.keyboard.write(text.upper()) # I must ALWAYS submit my answer via computer.keyboard.write.
```

...

User: Research each of the bullet points here and expand them.
You: I will research each bullet point.
```python
# I have manually read the text, so I will research each bullet point, print the results, and synthesize them myself.
print(computer.browser.search("The first bullet point's topic...
...
```
```output
The first bullet point refers to the... - Google
```
Now that I have researched each bullet point, I will write the result.
```python
computer.keyboard.write("- The modified first bullet point... # I must ALWAYS submit my answer via computer.keyboard.write.
...
```

Now, do this with the user's latest query as applied to the text above. Be concise and quick. No unnecessary actions. Use minimal characters. ALWAYS submit your answer via computer.keyboard.write.

The user cannot see your messages! They only see what you type via computer.keyboard.write(your_answer).

PLEASE ENSURE YOU RUN COMPUTER.KEYBOARD.WRITE(YOUR_ANSWER). You must actually type that.

'''.strip()

interpreter.system_message = "Respond with just the modification to the user's text. Don't respond with anything else."
interpreter.computer.languages = []

interpreter.llm.supports_functions = False
interpreter.llm.context_window = 16000
interpreter.llm.max_tokens = 2000
interpreter.llm.api_key = ""
interpreter.llm.model = "groq/llama3-8b-8192"

