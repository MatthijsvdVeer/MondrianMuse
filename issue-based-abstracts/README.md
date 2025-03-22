# Issue-Based Abstracts

This is the first version of the abstract generator. It works by running a workflow when a new GitHub issue is created. Three prompts are run in sequence to generate and review the abstract. The output of each prompt becomes a new comment on the issue.

Prompts:

- [Create Abstract][1]: This prompt creates the abstract based on the issue input.
- [Review Abstract][2]: Checks if the content from the issue made it into the abstract.
- [Writing Critic][3]: This prompt checks if the common words and phrases that GPT models like to use are present.

[1]: ./create-abstract.prompty
[2]: ./review-abstract.prompty
[3]: ./writing-critic.prompty
