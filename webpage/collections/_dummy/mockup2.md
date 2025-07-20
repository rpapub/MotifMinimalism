---
title: Versioning the Invocation
uuid: ab9432af-f7ee-488d-aa93-08ddc3ac53d1
level: Intermediate
created: 2025-07-19
authors:
  - Christian Prior-Mamulyan
audience:
  - Developer
downloads:
  - label: Version 0.1.21
    href: /webpage/download/Invocation_ad1e943f_v0.1.21.uis
  - label: Version 0.1.23
    href: /webpage/download/Invocation_ad1e943f_v0.1.23.uis
tech_stack:
  - UiPath Automation Cloud
  - Orchestrator 2024.10.0-s171
  - Studio v9e669382d
design_tool_versions:
  - UiPath Studio Web 9e669382d
  - https://uipath-apps-prdcom.azureedge.net/assetsdesignermfe/2025.7.14-11.8.26-s171.5d2e8d21b/v18/designerRemoteEntry.js
---

{% assign entry = site.data.solution_examples.merged.solution_examples[page.uuid] %}
{% assign sol = entry.solution %}
{% assign tested = sol.tested_with %}
{% assign downloads = sol.DownloadUrls %}
{% assign images = sol.images1 %}

# Versioning the Invocation

This example shows how input arguments—especially versioned fields—can be used to control logic branches at runtime. It demonstrates variations in how input values are bound and processed in orchestration triggers.

---

## 🔍 Description

{{ sol.Description }}

---

## 🖼️ Screenshots

{% include wa-carousel.html images=images %}

---

## 📦 Included Projects

### `MotifMinimalism`  
Type: `Process`  
Path: `MotifMinimalism/project.uiproj`  
Diagnostic utility for inspecting JSON payloads during BPMN orchestration. Focuses on traceability, schema inspection, and safe logging.

---

### `VersionString`  
Type: `ProcessOrchestration`  
Path: `VersionString/project.uiproj`  
Demonstrates passing a simple version string as an argument.  

```json
{
  "Version": "v1"
}
````

---

### `MultipleEntrypoints`

Type: `ProcessOrchestration`
Path: `MultipleEntrypoints/project.uiproj`
Three entry points:

* string only
* object only
* string + object

```json
{
  "Version": "v1"
}
```

---

### `RequestJObject`

Type: `ProcessOrchestration`
Path: `RequestJObject/project.uiproj`
Demonstrates structured JSON as input.

```json
{
  "Request": {
    "version": "",
    "correlationId": "",
    "requestId": "",
    "timestamp": "",
    "logContext": {},
    "payload": {}
  }
}
```

---

### `VersionAndRequestJObject`

Type: `ProcessOrchestration`
Path: `VersionAndRequestJObject/project.uiproj`
Combined typed input:

```json
{
  "Version": "vEmHQjakv",
  "Request": {
    "version": "",
    "correlationId": "",
    "requestId": "",
    "timestamp": "",
    "logContext": {},
    "payload": {}
  }
}
```

---

## 🧭 Runtime Construct Mapping

| Category               | Value                                  |
| ---------------------- | -------------------------------------- |
| **Construct**          | Invocation & Composition               |
| **Related Constructs** | Parameter Passing, Typing & Validation |
| **Execution Phase**    | Trigger-time                           |
| **Behavior**           | Input-driven branching and validation  |

---

## 📥 Downloads

{% include solution-examples-download.html downloads=downloads %}
