import re
import os

with open('/workspace/README.md', 'r') as f:
    content = f.read()

# 1. Add the warning
warning_text = """

> **⚠️ Avviso Importante:** Le repository di TRAE verranno purtroppo aggiornate meno di frequente. Attualmente sono molto occupato e, a livello personale, sto cercando un impiego (se conoscete qualcuno o se siete un'azienda che sta cercando personale) per potermi permettere una nuova casa. Finché non avrò raggiunto questa stabilità, il tempo da dedicare a GitHub sarà limitato e le repo TRAE verranno aggiornate purtroppo molto meno. Vi ringrazio per la comprensione! ❤️
"""
content = content.replace('# [TRAE](https://www.trae.ai/) Skills Collection', '# [TRAE](https://www.trae.ai/) Skills Collection' + warning_text)

# 2. Fix the "pallino" (blue diamond) in the first column
content = content.replace('**🔹 ️ Frontend**', '**🖥️ Frontend**')
content = content.replace('**🔹 ️ Architecture**', '**🏗️ Architecture**')
content = content.replace('**🔹 ️ Security**', '**🛡️ Security**')
content = content.replace('**🔹 🧪 Testing**', '**🧪 Testing**')

# Wait, let's also fix the fact that they are mixed. Actually, if I just replace them, they will have the correct emojis.
# Let's collect all AI Engineering files
ai_files = os.listdir('/workspace/ai_engineering')
ai_files = [f for f in ai_files if f.endswith('.md')]

# Generate AI Engineering rows
ai_rows = []
for i, file in enumerate(sorted(ai_files)):
    name = file.replace('.md', '').replace('_', ' ')
    # some custom names to match previous
    if file == 'Speech_to_Text_Whisper.md':
        name = 'Speech-to-Text Implementation (Whisper)'
    elif file == 'Local_LLM_Running_Ollama.md':
        name = 'Local LLM Running (Ollama)'
    elif file == 'Fine_tuning_Basics.md':
        name = 'Fine-tuning Basics'
    elif file == 'RAG_System_Architecture.md':
        name = 'RAG System Architecture'
    elif file == 'AI_Monitoring_Observability.md':
        name = 'AI Monitoring & Observability'
    elif file == 'AI_Safety_Ethics.md':
        name = 'AI Safety & Ethics'
    elif file == 'AI_Testing_Evaluation.md':
        name = 'AI Testing & Evaluation'
    elif file == 'Fine_Tuning_Custom_Models.md':
        name = 'Fine-Tuning Custom Models'
        
    category = '**🤖 AI Engineering**' if i == 0 else ''
    row = f"| {category} | {name} | [ℹ️](./ai_engineering/{file}) | [👆 View](./ai_engineering/{file}) |"
    ai_rows.append(row)

ai_section_str = '\n'.join(ai_rows)

# Replace the old AI Engineering section
# Find the start and end of AI Engineering section in the table
lines = content.split('\n')
new_lines = []
in_ai_section = False
for line in lines:
    if '| **🤖 AI Engineering** |' in line:
        in_ai_section = True
        new_lines.append(ai_section_str)
        continue
    
    if in_ai_section:
        if line.startswith('|') and ('**' in line.split('|')[1] or line.split('|')[1].strip() == ''):
            # Check if we moved to the next category
            cat_cell = line.split('|')[1].strip()
            if cat_cell != '' and cat_cell != '**🤖 AI Engineering**':
                in_ai_section = False
                new_lines.append(line)
        else:
            if not line.startswith('|'):
                in_ai_section = False
                new_lines.append(line)
    else:
        new_lines.append(line)

with open('/workspace/README.md', 'w') as f:
    f.write('\n'.join(new_lines))

print("README updated successfully.")
