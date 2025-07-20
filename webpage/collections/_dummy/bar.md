---
title: Invocation_ad1e943f
uuid: ab9432af-f7ee-488d-aa93-08ddc3ac53d1
---

{% assign entry = site.data.solution_examples.merged.solution_examples[page.uuid] %}
{% assign sol = entry.solution %}
{% assign tested = sol.tested_with %}
{% assign downloads = sol.DownloadUrls %}
{% assign images = sol.images1 %}


{% include wa-carousel.html images=images %}

<wa-divider></wa-divider>

<div class="wa-stack">
  <h3 class="wa-heading-m">Solution Info</h3>
  <p class="wa-caption-m">Overview of the solution and download details.</p>
  <wa-divider></wa-divider>
  <dl class="wa-stack wa-gap-2xl">
    <div class="wa-flank" style="--flank-size: 20ch;">
      <dt>Name</dt>
      <dd>{{ sol.Name }}</dd>
    </div>
    <div class="wa-flank wa-align-items-start" style="--flank-size: 20ch;">
      <dt>Description</dt>
      <dd>{{ sol.Description }}</dd>
    </div>
    <div class="wa-flank" style="--flank-size: 20ch;">
      <dt>    {% if sol.Author.size > 1 %}
      Authors
    {% else %}
      Author
    {% endif %}</dt>
      <dd>{{ sol.Authors | join: ", " }}</dd>
    </div>
    <div class="wa-flank" style="--flank-size: 20ch;">
      <dt>Created At</dt>
      <dd>{{ sol.created_at }}</dd>
    </div>
<div class="wa-flank" style="--flank-size: 20ch;">
  <dt>Tech Stack</dt>
  <dd>
    <ul>
      <li><strong>Name:</strong> {{ sol.tech_stack.name }}</li>
      <li><strong>Account Type:</strong> {{ sol.tech_stack.account_type }}</li>
      <li><strong>Orchestrator Version:</strong> {{ sol.tech_stack.orchestrator_version }}</li>
<!--      <li><strong>Studio Version:</strong> {{ sol.tech_stack.studio_version }}</li> -->
<li><strong>Design Tool Versions:</strong>
  <ul>
    <li>{{ sol.tech_stack.design_tool_versions[0] }}</li>
<!--    <li>{{ sol.tech_stack.design_tool_versions[1] }}</li>-->
  </ul>
</li>
    </ul>
  </dd>
</div>

<div class="wa-flank wa-align-items-start" style="--flank-size: 20ch;">
  <dt>Download</dt>
  <dd>
    <wa-card>
      <div class="wa-stack">
        {% for url in downloads %}
          <div class="wa-flank">
            <wa-icon name="paperclip"></wa-icon>
            <div class="wa-split">
              <span class="wa-caption-m wa-cluster">
                <span>{{ url | split: '/' | last }}</span>
                <span>—</span>
              </span>
              <wa-button
                appearance="plain"
                variant="brand"
                size="small"
                href="{{ url | absolute_url }}"
              >
                Download
              </wa-button>
            </div>
          </div>
          {% unless forloop.last %}
            <wa-divider></wa-divider>
          {% endunless %}
        {% endfor %}
      </div>
    </wa-card>
  </dd>
</div>
  </dl>
</div>



<wa-divider></wa-divider>

<h2>What is inside?</h2>

<wa-tab-group>
  {% for project in sol.Projects %}
    {% assign tab_name = project.Name | default: "Unnamed" | slugify %}
    <wa-tab panel="{{ tab_name }}">{{ project.Name | default: "Unnamed Project" }}</wa-tab>
  {% endfor %}

  {% for project in sol.Projects %}
    {% assign tab_name = project.Name | default: "Unnamed" | slugify %}
    <wa-tab-panel name="{{ tab_name }}">
      <h3>{{ project.Name | default: "Unnamed Project" }}</h3>

      <p><strong>Type:</strong> {{ project.Type }}</p>
      <p><strong>Description:</strong> {{ project.Description }}</p>
{% if project.inputs %}
  <h4>Inputs</h4>
  <wa-codeblock lang="json">{{ project.inputs | jsonify }}</wa-codeblock>
{% endif %}

{% if project.outputs %}
  <h4>Outputs</h4>
  <wa-codeblock lang="json">{{ project.outputs | jsonify }}</wa-codeblock>
{% endif %}

<!--      <p><strong>ID:</strong> {{ project.Id }}</p>
      <p><strong>Path:</strong> {{ project.ProjectRelativePath }}</p>
      <p><strong>Studio Version:</strong> {{ project.studioVersion }}</p>
      <p><strong>Project Version:</strong> {{ project.projectVersion }}</p>
      <p><strong>Framework:</strong> {{ project.targetFrameworkValue }}</p>-->

{% include wa-carousel.html images=project.images %}
    </wa-tab-panel>
  {% endfor %}
</wa-tab-group>

