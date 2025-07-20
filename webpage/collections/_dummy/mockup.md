---

title: "Parallel Queue Processing – MCVE"
---

{% assign demo_images = "capture_001_18072025_232409.png,capture_003_18072025_232452.png,capture_004_18072025_232456.png,capture_005_18072025_232522.png,capture_006_18072025_232531.png" | split: "," %}
{% include wa-carousel.html images=demo_images %}

<wa-divider></wa-divider>

## 🧩 What problem does this solve?

You need to process multiple tasks in parallel — but not all at once. This solution shows how to coordinate concurrent jobs using queues and a semaphore.

---

## 🔍 When would I use this?

- Processing 100s of PDFs or web pages concurrently  
- Managing limited licenses or compute resources  
- Controlling concurrency across distributed bots

---

## 📦 What’s inside?

The solution ZIP contains:

- `Dispatcher` – adds items to a processing queue  
- `Worker` – triggered by queue, does the job  
- `Semaphore Asset` – shared control to limit concurrent runs

---

## 🚀 How do I use it?

1. Import the ZIP into your automation environment  
2. Set up:
   - A queue named `WorkItems`
   - An asset named `ConcurrentSlots` (Int, e.g., 3)
3. Start the `Dispatcher`
4. Workers will pick up items with respect to the semaphore

---

## ✅ What should I observe?

- Queue gets populated
- 3 workers run in parallel (if semaphore = 3)
- As jobs complete, others are released

---

## 🛠️ Runtime Constructs used

- **Queue Trigger**
- **Semaphore Asset**
- **For Each Parallel**
- **Delay (for simulation)**

---

## 📥 Download

<wa-card>
  <div class="wa-flank">
    <wa-icon name="paperclip"></wa-icon>
    <div class="wa-split">
      <span class="wa-caption-m">parallel-queue-example.zip</span>
      <wa-button
        appearance="plain"
        variant="brand"
        size="small"
        href="/assets/solutions/parallel-queue-example.zip"
      >
        Download
      </wa-button>
    </div>
  </div>
</wa-card>

---

## 🔗 Related

- [Runtime Construct: Queue Trigger](/docs/runtime-constructs/queue-trigger)  
- [Pattern: Semaphore with Assets](/docs/patterns/semaphore-asset)  
- [Example: Batch Processing](/solutions/batching)

