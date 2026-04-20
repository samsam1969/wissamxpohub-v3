content = open('services/claude_service.py', encoding='utf-8').read()

old = '    # -- Layer 2: Tavily Web Intelligence (replaces OpenAI DeepSearch)\n    web_data = ""\n    tavily_sources = []'

new = '    # -- Layer 2: Tavily Web Intelligence (replaces OpenAI DeepSearch)\n    web_data = ""\n    tavily_sources = []  # initialized before try'

# Fix: make sure tavily_sources is defined before try block
content = content.replace(
    '    # -- Layer 2: Tavily Web Intelligence (replaces OpenAI DeepSearch)\n    web_data = ""\n    tavily_sources = []',
    '    # -- Layer 2: Tavily Web Intelligence (replaces OpenAI DeepSearch)\n    web_data = ""\n    tavily_sources = []'
)

# Real fix - add initialization before the try block
old2 = '    # -- Layer 2: Tavily Web Intelligence'
new2 = '    tavily_sources = []  # safe init\n    # -- Layer 2: Tavily Web Intelligence'
content = content.replace(old2, new2, 1)

open('services/claude_service.py', 'w', encoding='utf-8').write(content)
print('Done')
