---
layout: webawesome
---

{% assign entry = site.data.solution_examples.merged.solution_examples[page.uuid] %}
{% assign sol = entry.solution %}
{% assign downloads = sol.download_urls %}
{% assign images = sol.images %}
{% assign active = page.active_project %}

{{ entry.publishing.summary }}

<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

{%- comment -%}
  Carousel viewer for solution-level images.
{%- endcomment -%}
{% include wa-carousel.html images=images unique_id=page.uuid %}

<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

{% include solution-examples-details.html entry=entry %}

<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

<h2>What is inside?</h2>

{% include solution-examples-projects.html sol=sol active=active %}

<h2>How to use?</h2>

Download the solution from the links above, import into your Automation Cloud and inspect the contents.
