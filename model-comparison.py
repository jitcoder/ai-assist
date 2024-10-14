import ollama
import json
import os
import sys

def load_context():
  if not os.path.exists("history.context"):
    return None
  with open("history.context", 'r') as file:
      context_data = json.load(file)  # Assuming the file is JSON-formatted
  return context_data

def save_context(context):
  with open("history.context", 'w') as file:
    json.dump(context, file)


def test_context(model:str):
  print(f"### Model {model} ###")
  context = None
  stream = ollama.generate(
    model=model,
    prompt="whats the iptables command to list all rules?",
    stream=True
  )

  for resp in stream:
    if 'context' in resp:
      context = resp['context']
      break
    if resp['done'] == False:
      sys.stdout.write(resp['response'])

  stream = ollama.generate(
    model=model,
    prompt="what about nat",
    context=context,
    stream=True
  )

  for resp in stream:
    if 'context' in resp:
      context = resp['context']
      break
    if resp['done'] == False:
      sys.stdout.write(resp['response'])
  print(f"\n##############\n")
models = ollama.list()
for model in models['models']:
  test_context(model['name'])