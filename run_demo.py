
from langgraph_builder import LangGraphExecutor
import json, os
ex = LangGraphExecutor()
ex.run()
outf = os.path.join(os.path.dirname(__file__), 'run_context.json')
with open(outf, 'w', encoding='utf-8') as f:
    json.dump(ex.context, f, indent=2)
print('\nSaved run_context.json in project root.')
