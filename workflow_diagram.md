flowchart TD
  writer["writer (Start)"];
  reviewer["reviewer"];
  internal_writer --> writer;
  internal_reviewer --> reviewer;
  writer --> reviewer;