---
name: inspect-dependencies
description: Analyze a file's internal structure and project-local dependency graph. Use when the user asks to inspect, visualize, map, or explain dependencies for a specific file or module.
---

# Inspect Dependencies

Analyze the requested file without modifying files.

## Procedure

1. Confirm the path exists. If not, report `파일을 찾을 수 없습니다: <path>`.
2. Identify language, file type, approximate size, and likely dependency syntax.
3. Parse project-local dependencies:
   - JS/TS/Vue: `import`, `require`, script blocks, component references.
   - Python: `import`, `from ... import`.
   - Go: `import`.
   - Java/Kotlin: `import`.
   - Rust: `use`, `mod`.
   - C/C++: `#include`.
   - YAML/Docker/config: includes, copied files, referenced paths.
4. Resolve relative paths and common aliases from local config files such as `tsconfig`, Vite, webpack, or package workspace settings.
5. Separate internal project files from external packages.
6. If recursive analysis is requested, traverse internal dependencies and stop on cycles.

## Output

Default to:

- dependency tree
- one-line summary per internal file
- external package list
- cycle or unreadable-file notes

Keep the tree compact and use plain ASCII indentation.

For detailed analysis, include exports, major functions/classes, role, dependencies, and line count per file.

If the dependency set exceeds about 50 files, pause and ask before continuing deeper analysis.
