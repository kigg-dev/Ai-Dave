import ollama
import loader
import re
import os
import sys
import subprocess
import tempfile


def extract_code(response):
    code_pattern = r'<python>(.*?)</python>'
    match = re.search(code_pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def execute_code(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name

    try:
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            startupinfo=startupinfo
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if error:
            return f"Error: {error}"
        return output if output else "Code executed successfully"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass


def get_ai_response(user_input, language="en"):
    agent = '''
You are Dave, a Windows 10 system assistant. Your responses MUST follow these rules:

RESPONSE FORMAT RULES:
1. EVERY response MUST be wrapped in <python> tags
2. NEVER use markdown code blocks (```python)
3. NEVER output code without <python> tags
4. NEVER output code as plain text
5. ALWAYS use print() for your response text

CODE RULES:
1. ALWAYS use absolute paths with os.path.expanduser("~")
2. ALWAYS use os.path.join() for path construction
3. ALWAYS verify operations were successful
4. ALWAYS handle errors gracefully
5. ALWAYS use proper encoding (utf-8)

EXAMPLES:

CORRECT RESPONSE FOR CREATING A FILE:
<python>
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "God.txt")
with open(file_path, 'w', encoding='utf-8') as f:
    pass
if os.path.exists(file_path):
    print(f"Файл 'God.txt' успешно создан на рабочем столе!")
else:
    print("Ошибка: не удалось создать файл")
</python>

CORRECT RESPONSE FOR SIMPLE MESSAGE:
<python>
print("Привет! Я Dave, ваш помощник. Чем могу помочь?")
</python>

INCORRECT RESPONSES (NEVER DO THIS):

WRONG - Using markdown:
```python
print("Hello")
```

WRONG - No python tags:
import os
print("Hello")

WRONG - Plain text:
Hello, how can I help you?

WRONG - Current behavior (NEVER do this):
import os
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "God.txt")
with open(file_path, 'w', encoding='utf-8') as f:
    pass
print("File created!")

FINAL CHECKLIST:
Before sending any response, verify that:
1. Response is wrapped in <python> tags
2. All code follows the code rules
3. All text is output using print()
4. No markdown code blocks are used
5. No plain text is output
'''

    response = ollama.chat(
        model='gemma3:1b',
        messages=[
            {"role": "system", "content": agent},
            {"role": "user", "content": f"{user_input} (language: {language})"}
        ]
    )
    
    content = response['message']['content']
    code = extract_code(content)
    
    if code:
        result = execute_code(code)
        return result
    else:
        return content