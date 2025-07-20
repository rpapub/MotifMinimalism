---
layout: webawesome
---


{% assign entry = site.data.solution_examples.merged.solution_examples[page.uuid] %}
{% assign sol = entry.solution %}
{% assign tested = sol.tested_with %}
{% assign downloads = sol.DownloadUrls %}
{% assign images = sol.images1 %}
{% assign active = page.active_project %}


{{ entry.publishing.summary }}

<div style="margin-block: 2rem;">
  <!-- content here -->
</div>

{% include wa-carousel.html images=images %}

<div style="margin-block: 2rem;">
  <!-- content here -->
</div>

{% include solution-examples-details.html entry=entry %}

<div style="margin-block: 2rem;">
  <!-- content here -->
</div>

<h2>What is inside?</h2>

{% include solution-examples-projects.html sol=entry.solution active=active_project %}
