# File Reading

Read files with purpose. Before reading a file, know what you're looking for.
Use Grep to locate relevant sections before reading entire large files.
Never re-read a file you've already read in this session.
For files over 500 lines, use offset/limit to read only the relevant section.

## Why

Without these constraints, the model tends to "open the file and see what's inside" — burning context on bytes it never needed. The system prompt forbids re-reading after edits, but does not cover pre-read economy (purposeful reads, Grep-first, offset/limit). Re-evaluate when the model consistently applies these habits on its own.
