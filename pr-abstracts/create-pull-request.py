import argparse
import json
import re
import os
import subprocess
from datetime import datetime
from pathlib import Path
from promptflow.core import tool, Prompty

folder = Path(__file__).parent.absolute().as_posix()

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

def sanitize_filename(title):
   # Remove emojis and special characters
   title = re.sub(r'[^\w\s-]', '', title)
   # Replace spaces with hyphens
   title = re.sub(r'\s+', '-', title)
   # Convert to lowercase for consistency
   return title.lower()

def run_command(command):
    """Run a command and return the output"""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("--answers", default="", help="The answers to the questions for the session.")
   args = parser.parse_args()

   result = flow_entry(answers=args.answers)
   
   # Parse the JSON result
   parsed_result = json.loads(result)
   
   # Extract title and abstract
   title = parsed_result.get("title", "")
   abstract = parsed_result.get("abstract", "")
   
   # Print the extracted values
   print(f"Title: {title}")
   print(f"Abstract: {abstract}")
   
   # Create abstracts directory if it doesn't exist
   abstracts_dir = os.path.join(os.path.dirname(folder), "abstracts")
   os.makedirs(abstracts_dir, exist_ok=True)
   
   # Sanitize the title for filename
   filename = sanitize_filename(title)
   
   # Create markdown file
   file_path = os.path.join(abstracts_dir, f"{filename}.md")
   
   # Write abstract to the file
   with open(file_path, "w") as f:
       f.write(abstract)
   
   print(f"Created abstract file: {file_path}")
   
   # Get the repo root directory
   repo_root = Path(folder).parent.absolute()
   os.chdir(repo_root)
   
   # Create a branch name based on sanitized title and timestamp
   timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
   branch_name = f"abstract/{filename[:40]}-{timestamp}"
   
   # Create a new git branch
   print(f"Creating git branch: {branch_name}")
   run_command(["git", "checkout", "-b", branch_name])
   
   # Add the new file to git
   run_command(["git", "add", file_path])
   
   # Commit with appropriate message
   commit_message = f"✏️ Add abstract: {title}"
   print(f"Committing with message: {commit_message}")
   run_command(["git", "commit", "-m", commit_message])
   
   # Push the branch
   print("Pushing to remote repository...")
   run_command(["git", "push", "-u", "origin", branch_name])
   
   # Create a pull request using GitHub CLI
   print("Creating pull request...")
   pr_result = run_command(["gh", "pr", "create", "-f"])
   
   if pr_result:
       print(f"Successfully created pull request: {pr_result}")
       print(f"PR_URL={pr_result}")  # Add this line to output the PR URL in an easily extractable format
   else:
       print("Failed to create pull request. You may need to create it manually.")
   
   print(f"Successfully created branch '{branch_name}' and pushed it to the remote repository")
   
   # Return the PR result
   exit(0 if pr_result else 1)
