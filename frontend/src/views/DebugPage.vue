<template>
  <div class="debug-page layout-contained layout-spacing-bottom">
    <header class="layout-spacing-top">
      <h1>System Style Guide Debugger</h1>
      <p class="subtle">Use this workspace to verify typography scales, dark/light global tokens, interaction states, and design system utilities.</p>
    </header>

    <hr />

    <!-- Typography Section -->
    <section class="layout-spacing-top">
      <h2>1. Typography & Hierarchy</h2>
      <div class="card grid-2">
        <div class="flex-col gap-xs">
          <h1>Heading 1 (fs-4)</h1>
          <h2>Heading 2 (fs-3)</h2>
          <h3>Heading 3 (fs-2)</h3>
          <h4>Heading 4 (fs-1)</h4>
          <h5>Heading 5 (fs-0)</h5>
          <h6>Heading 6 (fs-neg-1)</h6>
        </div>
        <div class="flex-col gap-md">
          <p class="no-top">Standard paragraph text using <code>--fs-0</code>. This shows standard line height and font weight behaviors across normal copy strings.</p>
          <div>
            <label>Standard Form Label Element</label>
            <p>
              <a href="#" @click.prevent>Standard Underline Link</a> or a 
              <a href="#" class="hover-line" @click.prevent>Link with .hover-line utility</a>
            </p>
          </div>
          <p class="subtle">Text using the <code>.subtle</code> class modification.</p>
          <p class="soft">Text using the <code>.soft</code> class modification.</p>
        </div>
      </div>
    </section>

    <!-- Interactive Elements Section -->
    <section class="layout-spacing-top">
      <h2>2. Interactive Elements (The 5 Button Stack)</h2>
      <div class="card">
        <div class="button-grid-header">
          <span>Button Variant Style</span>
          <span>Normal State</span>
          <span>Disabled State</span>
        </div>
        
        <div class="button-matrix">
          <!-- 1. Primary -->
          <div class="button-row">
            <div class="variant-info">
              <strong>Primary Dark</strong>
              <span class="subtle">High emphasis main CTA</span>
            </div>
            <div><button class="btn-primary">Save Changes</button></div>
            <div><button class="btn-primary" disabled>Save Changes</button></div>
          </div>

          <!-- 2. Outline -->
          <div class="button-row">
            <div class="variant-info">
              <strong>Secondary Outline</strong>
              <span class="subtle">Medium emphasis, borders only</span>
            </div>
            <div><button class="btn-outline">Cancel Action</button></div>
            <div><button class="btn-outline" disabled>Cancel Action</button></div>
          </div>

          <!-- 3. Neutral -->
          <div class="button-row">
            <div class="variant-info">
              <strong>Neutral Gray Fill</strong>
              <span class="subtle">Medium-low emphasis card action</span>
            </div>
            <div><button class="btn-neutral">Edit Profile</button></div>
            <div><button class="btn-neutral" disabled>Edit Profile</button></div>
          </div>

          <!-- 4. Text -->
          <div class="button-row">
            <div class="variant-info">
              <strong>Text Link Style</strong>
              <span class="subtle">Low emphasis quiet utility</span>
            </div>
            <div><button class="btn-text">Learn More</button></div>
            <div><button class="btn-text" disabled>Learn More</button></div>
          </div>

          <!-- 5. Destructive -->
          <div class="button-row">
            <div class="variant-info">
              <strong>Destructive Red</strong>
              <span class="subtle">Critical emphasis permanent danger</span>
            </div>
            <div><button class="btn-negative">Delete Account</button></div>
            <div><button class="btn-negative" disabled>Delete Account</button></div>
          </div>
        </div>

        <!-- Extra Button Utilities -->
        <div class="button-utilities">
          <span class="section-label">Shape Options</span>
          <div class="flex-row gap-sm">
            <button class="btn-neutral btn-pill">Pill Shape Variant</button>
            <button class="btn-primary btn-pill">Pill Shape Primary</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Forms & Inputs Section -->
    <section class="layout-spacing-top">
      <h2>3. Forms & Inputs</h2>
      <div class="card grid-2">
        <form @submit.prevent>
          <h3>Example Form Spec</h3>
          
          <label for="input-normal">Text Input (Default)</label>
          <input id="input-normal" type="text" placeholder="Enter text context..." />

          <label for="select-normal">Selection Field</label>
          <select id="select-normal">
            <option>Option Variable One</option>
            <option>Option Variable Two</option>
          </select>

          <label for="input-invalid">Invalid State Simulation</label>
          <input id="input-invalid" type="text" required placeholder="Delete text to trigger error state..." value="Clear me out" />

          <div class="checkbox-row">
            <input id="check-1" type="checkbox" checked />
            <label for="check-1">Keep user sessions signed in securely</label>
          </div>
        </form>

        <div>
          <h3>Description List Layout</h3>
          <dl>
            <dt>Account Status</dt>
            <dd>Premium Tier Account</dd>
            <dt>Renewal Date</dt>
            <dd>June 30, 2026</dd>
            <dt>System Identity</dt>
            <dd>Operational Node</dd>
          </dl>
        </div>
      </div>
    </section>

    <!-- Utilities Section -->
    <section class="layout-spacing-top">
      <h2>4. UI Utilities & Indicators</h2>
      <div class="card grid-2">
        <div>
          <h3>Badges System</h3>
          <div class="flex-row gap-sm align-center">
            <span class="badge">Default Grey</span>
            <span class="badge badge-primary">Primary Status</span>
            <span class="badge badge-positive">Success Badge</span>
            <span class="badge badge-warning">Warning State</span>
            <span class="badge badge-negative">Error Alert</span>
          </div>
          
          <p class="subtle" style="margin-top: var(--spacing-md); margin-bottom: var(--spacing-sm);">Small sizing variants:</p>
          <div class="flex-row gap-sm align-center">
            <span class="badge badge-sm">Base SM</span>
            <span class="badge badge-sm badge-positive">Success SM</span>
            <span class="badge badge-sm badge-negative">Failure SM</span>
          </div>

          <p style="margin-top: var(--spacing-md);">Inline divider separation: <span>Item One</span> <span class="seperator">|</span> <span>Item Two</span></p>
        </div>

        <div class="flex-col gap-md">
          <div>
            <h3>Disclosures & Loading States</h3>
            <details>
              <summary>Click to disclose accordion contents</summary>
              <div class="content">
                <p>This panel shows the interior layout architecture inside localized summary detail containers.</p>
              </div>
            </details>
          </div>

          <div class="flex-col gap-xs">
            <label>Loading Wave Skeleton Simulator</label>
            <div class="loading-wave skeleton-bar"></div>
            <div class="loading-wave skeleton-bar short"></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--spacing-lg);
}

/* Button Debug Grid Matrix Layout structures */
.button-grid-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid var(--c-border);
  font-size: var(--fs-neg-2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-text-subtle);
  font-weight: 700;
}

.button-matrix {
  display: flex;
  flex-direction: column;
}

.button-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  align-items: center;
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--c-border);
}

.button-row:last-child {
  border-bottom: none;
}

.variant-info {
  display: flex;
  flex-direction: column;
}

.variant-info strong {
  color: var(--c-text-strong);
  font-size: var(--fs-0);
}

.variant-info .subtle {
  font-size: var(--fs-neg-2);
}

.button-utilities {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-md-lg);
  border-top: 1px dashed var(--c-border);
}

.section-label {
  display: block;
  font-size: var(--fs-neg-2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-text-subtle);
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
}

.skeleton-bar {
  height: 16px;
  border-radius: var(--border-radius-sm);
  width: 100%;
}

.skeleton-bar.short {
  width: 60%;
}
</style>