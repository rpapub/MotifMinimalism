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
{% include wa-carousel.html images=images solution_id=page.uuid unique_id=page.uuid %}

<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

{% include solution-examples-details.html entry=entry %}

<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

<h2>What is inside?</h2>

{% include solution-examples-projects.html sol=sol active=active solution_id=page.uuid observations=entry.observations %}



<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

{% if entry.publishing.citation_ids and entry.publishing.citation_ids.size > 0 %}
    <h2>Further Reading</h2>
    <p class="wa-caption-m">Related resources and references.</p>
    <wa-divider></wa-divider>
    {% include citations.html ids=entry.publishing.citation_ids %}
{% endif %}



<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

<h2>Observations</h2>

{% include solution-examples-observations.html observations=entry.observations random_render_id="A7F2X9" %}

<div style="margin-block: 2rem;">
  <!-- Additional content -->
</div>

<h2>How to use?</h2>

Download the solution from the links above, import into your Automation Cloud and inspect the contents.

