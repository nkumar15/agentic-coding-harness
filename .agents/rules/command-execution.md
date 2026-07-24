# Command Execution

Shared command discipline for agents and roles.

## Shell Calls

- Run one simple command per shell call.
- Run verification commands in the foreground and wait for them to finish.
- Do not background commands with `&` or a background-tool option.
- Do not poll long-running commands with custom `while`, `sleep`, or process loops unless the
  project conventions explicitly define that polling command as a gate command.
- Read command results afterward with a separate simple command such as `cat`, `find`, `rg`, `tail`,
  or the host-provided command output.
- Do not use command substitution such as `$(...)`.
- Do not chain commands with `&&`, `;`, or `|` inside agent-authored workflow commands.
- Do not prefix commands with `cd`; use the repository root as the working directory unless the
  host execution API provides a working-directory parameter.

## Source Of Truth

When a gate declares commands in `.agents/process/gates.yaml`, run the commands from the gate
definition exactly after resolving placeholders from project conventions. Do not copy command
strings into role instructions or rely on remembered commands from another repository.

If a gate command contains placeholders such as `<global-check-command>`, `<domain-module>`, or
`<api-base-url-env-var>`, resolve them from the active work item, the approved design, and the
relevant conventions file before execution. Record the resolved command in the gate report.
