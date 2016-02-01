PyOS is mostly cross-platform. The only part that will likely need to be rewritten is the kernel itself and the stdio library, which bypasses the kernel-level IO abstractions. A few programs may depend on system configuration and need to be rebuilt, but for the most part it should work without much modification.

stdio assumes that it is running on top of an ANSI-compatible terminal, and both the kernel and stdio rely on a certain way that the filesystem must be presented.
