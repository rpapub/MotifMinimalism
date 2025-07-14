# Fundamental Patterns Catalog

A structured collection of minimal software execution patterns, each demonstrated through focused, platform-specific examples.

> Exported solution artifacts (`.zip`) are published via the `gh-pages` branch as static deployment assets.  
> This serves as a lightweight delivery channel for runtime artifacts, decoupled from source code and versioned independently.

## 🎯 Purpose

This repository documents a **minimal set of execution primitives and composition units** that underpin all software systems and platforms. Each concept is illustrated with multiple minimal, focused examples—aimed at education, architecture analysis, and platform comparison.

---

## 📦 Repository Structure

Each **top-level folder** represents a fundamental execution unit.  
Each **subfolder** under a unit holds a self-contained example.
<!--
```bash
/
├── flow-control/
│   ├── 01-sequence/
│   ├── 02-conditional/
│   └── 03-looping/
├── parameter-passing/
│   ├── 01-basic-function-call/
│   ├── 02-default-values/
│   └── 03-named-arguments/
├── error-handling/
├── configuration/
├── state-memory/
├── invocation-composition/
├── event-handling/
├── debugging-observability/
├── versioning-reusability/
├── typing-validation/
└── docs/  # Optional: shared diagrams, lifecycle explanation, etc.
```
//-->

## 🧱 Execution Units Covered

| Unit                      | Status    | Description                               |
| ------------------------- | --------- | ----------------------------------------- |
| Flow Control              | ✅ Started | Sequence, branching, loops, concurrency   |
| Parameter Passing         | ✅ Started | Function calls, argument modes            |
| Error Handling            | ✅ Started | Exceptions, error propagation, retry      |
| Configuration             | 🚧 To do   | Static vs dynamic, hierarchical overrides |
| State & Memory            | 🚧 To do   | Variable scoping, mutation, persistence   |
| Invocation & Composition  | 🚧 To do   | Modularity, composition patterns          |
| Event Handling            | 🚧 To do   | Event sources, handlers, pub/sub          |
| Debugging & Observability | 🚧 To do   | Logging, tracing, runtime inspection      |
| Versioning & Reusability  | 🚧 To do   | Contracts, compatibility, modular reuse   |
| Typing & Validation       | 🚧 To do   | Type systems, runtime vs static checks    |

---

## 📚 Usage

Each example is:

* Minimal and self-contained
* Platform-agnostic when possible
* Includes a short `README.md` explaining the concept

🧪 To run examples, see `README.md` inside each subfolder.
📝 Articles or external references will be linked once available.

---

## 🔭 Future Work

* [ ] to do

---

## 🤝 Contributing

Contributions are welcome! Especially:

* Minimal working examples for missing units
* Comparative examples in different languages
* Real-world pattern applications

See `CONTRIBUTING.md` (📄 To be written).

---


## 📄 License

Licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENCE)
See [AUTHORS.md](AUTHORS.md) for contributors.