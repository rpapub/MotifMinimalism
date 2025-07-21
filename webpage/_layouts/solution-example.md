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

{%- comment -%}
  Show a preview carousel for solution-level images with a fullscreen viewer.
  The UUID ensures correct syncing across carousels on the same page.
{%- endcomment -%}
{% include wa-carousel.html images=images unique_id=page.uuid %}

<div style="margin-block: 2rem;">
  <!-- content here -->
</div>

{% include solution-examples-details.html entry=entry %}

<div style="margin-block: 2rem;">
  <!-- content here -->
</div>

<h2>What is inside?</h2>

{% include solution-examples-projects.html sol=entry.solution active=active_project %}

<h2>How to use?</h2>

Download the solution from the links above, import into your Automation Cloud and inspect the contents.
