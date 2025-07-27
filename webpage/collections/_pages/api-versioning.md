---

title: "Why External APIs Should Always Include a Version"
permalink: /explainer/api-versioning/
published: true
description: "API versioning isn't just a nice-to-have—it's a contract with your users. Here's why it matters."
---

APIs are promises. Once exposed to external clients, any change—however small—can break something. That’s where **API versioning** becomes essential.

## What Is API Versioning?

It’s the practice of tagging your API with a version (like `v1`, `v2`, or `2025-07`) in the URL, headers, or payload. This small addition protects clients from unexpected changes and gives you room to grow.

## Why It Matters

Without versioning, every change is a risk. With it:

* You can **iterate without breaking** existing clients.
* Users can **upgrade on their schedule**.
* You can **retire old versions gradually**, not abruptly.
* Support and debugging become **simpler and more predictable**.
* Documentation stays **clean and focused per version**.

API versioning isn't overhead—it's stability, flexibility, and respect for your users.

## Try This

* Add `version` to your payload.
* Later, Document what changes in `v2/`.
* Never make breaking changes to a live version. Add a new one.

This one step turns your callables from fragile to future-proof.
