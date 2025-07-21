---
title: FAQ
permalink: /resources/faq/
---

<div class="wa-stack">
  <h2>Publishing</h2>

  <wa-details appearance="plain">
    <h3 slot="summary" class="wa-heading-m" style="margin: 0">How are solutions structured and displayed?</h3>
    Each solution is defined in a JSON file under <code>_data</code>, including metadata, images, and projects. Jekyll renders this into a rich HTML interface using components like <code>&lt;wa-tab-group&gt;</code> and <code>&lt;wa-carousel&gt;</code>.
  </wa-details>
  <wa-divider></wa-divider>

  <wa-details appearance="plain">
    <h3 slot="summary" class="wa-heading-m" style="margin: 0">Where do solution images need to be stored?</h3>
    Images listed in the JSON (e.g., <code>images1</code>, <code>images</code>) must be placed in <code>/assets/dummy/</code> to match the resolved image paths during site generation.
  </wa-details>
  <wa-divider></wa-divider>

  <wa-details appearance="plain">
    <h3 slot="summary" class="wa-heading-m" style="margin: 0">How do I add a new solution?</h3>
    Add a structured JSON file (e.g., <code>example.json</code>) to <code>_data/dummy/</code>. Reference it in a Jekyll page, and it will render automatically using the existing layouts.
  </wa-details>
  <wa-divider></wa-divider>

  <wa-details appearance="plain">
    <h3 slot="summary" class="wa-heading-m" style="margin: 0">Why isn’t my <code>_testcollection</code> page rendering?</h3>
    Check that the file is in <code>webpage/collections/_testcollection/</code>, has front matter, and that the collection is defined with <code>output: true</code> in <code>_config.yml</code>. Also verify a valid layout is applied.
  </wa-details>
</div>




<div class="wa-stack">
  <h2>Publishing</h2>

  <wa-details appearance="plain">
    <h3 slot="summary" class="wa-heading-m" style="margin: 0">How do I get the version of Studio Web that code was tested with?</h3>
    When in Studio Web, open the Browser's Inspector, and in the Network traffic look for for a request to version.json, at the URL https://cloud.uipath.com/rpapub/studio_/version.json The response is a alphanumerical string, on 2025-07-19 it was "9e669382d". Reference this as the version of Studio Web that the code was tested with.
  </wa-details>
  <wa-divider></wa-divider>

  <wa-details appearance="plain">
    <h3 slot="summary" class="wa-heading-m" style="margin: 0">How do I get the version of Orchestrator that code was tested with?</h3>
    In UiPath Orcehstrator, e.g. at the URL https://cloud.uipath.com/$organization/$tenant/orchestrator_/, Click on the user profile image link in the top right corder of the page, then the version is show. Example: Orchestrator 2024.10.0-s171.9492 
  </wa-details>
  <wa-divider></wa-divider>

</div>