import ollama
import json
import os
import sys
import argparse

def load_context():
  if not os.path.exists("history.context"):
    return None
  with open("history.context", 'r') as file:
      context_data = json.load(file)  # Assuming the file is JSON-formatted
  return context_data

def save_context(context):
  with open("history.context", 'w') as file:
    json.dump(context, file)

context = load_context()
parser = argparse.ArgumentParser()
parser.add_argument('--prompt', type=str)
parser.add_argument('--model', type=str, default="gem")
args = parser.parse_args()

stream = ollama.generate(
  model=args.model,
  prompt=args.prompt,
  context=context,
  stream=True
)

iterations = 0
for resp in stream:
  iterations += 1
  if 'context' in resp:
    context = resp['context']
    break
  if resp['done'] == False:
    sys.stdout.write(resp['response'])
    sys.stdout.flush()

sys.stdout.write("\n")

if context is not None:
  save_context(context)
