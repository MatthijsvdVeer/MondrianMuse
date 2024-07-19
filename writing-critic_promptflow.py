import json

from pathlib import Path
folder = Path(__file__).parent.absolute().as_posix()

from promptflow.core import tool, Prompty

@tool
def flow_entry(    
      abstract: any
) -> str:
  # path to prompty (requires absolute path for deployment)
  path_to_prompty = folder + "/writing-critic.prompty"

  # load prompty as a flow
  flow = Prompty.load(path_to_prompty)
 
  # execute the flow as function
  result = flow(
    abstract = abstract
  )

  return result

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("--abstract", default="", help="The abstract that was created.")
   args = parser.parse_args()

   result = flow_entry(abstract=args.abstract)
   print(result)
