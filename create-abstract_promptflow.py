import json
import argparse

from pathlib import Path
folder = Path(__file__).parent.absolute().as_posix()

from promptflow.core import tool, Prompty

@tool
def flow_entry(    
      answers: any
) -> str:
  # path to prompty (requires absolute path for deployment)
  path_to_prompty = folder + "/create-abstract.prompty"

  # load prompty as a flow
  flow = Prompty.load(path_to_prompty)
 
  # execute the flow as function
  result = flow(
    answers = answers
  )

  return result

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("--answers", default="", help="The answers to the questions for the session.")
   args = parser.parse_args()

   result = flow_entry(topic=args.answers)
   print(result)
