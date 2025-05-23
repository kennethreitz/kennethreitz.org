/**
 * Tufte CSS Converter
 * A utility to enhance markdown content with Tufte CSS features
 * 
 * This script converts standard markdown content into Tufte-style content:
 * - Converts footnotes to sidenotes
 * - Enables margin notes from special syntax
 * - Enhances figures with proper layout
 * - Adds Tufte-style handling for tables and blockquotes
 */

document.addEventListener('DOMContentLoaded', function() {
  // Only run on pages with Tufte content
  if (!document.getElementById('tufte-body')) return;
  
  // Convert footnotes to sidenotes
  convertFootnotesToSidenotes();
  
  // Process margin notes
  processMarginNotes();
  
  // Process full-width elements
  processFullWidthElements();
  
  // Process figures and images
  processFigures();
  
  // Add table captions
  processTableCaptions();
  
  // Process special blockquotes
  processBlockquotes();
});

/**
 * Converts Markdown-style footnotes to Tufte-style sidenotes
 */
function convertFootnotesToSidenotes() {
  // Find all footnote references
  const footnoteRefs = document.querySelectorAll('a[href^="#fn"]');
  
  footnoteRefs.forEach((ref, index) => {
    // Get the footnote ID
    const fnId = ref.getAttribute('href').substring(1);
    const footnote = document.getElementById(fnId);
    
    if (!footnote) return;
    
    // Create the sidenote
    const sidenote = document.createElement('span');
    sidenote.className = 'sidenote';
    sidenote.innerHTML = footnote.innerHTML;
    
    // Create the sidenote number
    const sidenoteNumber = document.createElement('label');
    sidenoteNumber.className = 'margin-toggle sidenote-number';
    sidenoteNumber.setAttribute('for', `sidenote-${index}`);
    sidenoteNumber.textContent = (index + 1);
    
    // Create the toggle
    const toggle = document.createElement('input');
    toggle.type = 'checkbox';
    toggle.id = `sidenote-${index}`;
    toggle.className = 'margin-toggle';
    
    // Replace the footnote reference with our new elements
    ref.parentNode.insertBefore(sidenoteNumber, ref);
    ref.parentNode.insertBefore(toggle, ref);
    ref.parentNode.insertBefore(sidenote, ref.nextSibling);
    ref.remove();
    
    // Hide the original footnote
    if (footnote.parentNode) {
      footnote.parentNode.removeChild(footnote);
    }
  });
  
  // Remove the footnotes section if it exists and is now empty
  const footnoteSection = document.querySelector('.footnotes');
  if (footnoteSection && footnoteSection.querySelectorAll('li').length === 0) {
    footnoteSection.remove();
  }
}

/**
 * Process special margin note syntax: [MN] This is a margin note [/MN]
 */
function processMarginNotes() {
  // Find all paragraphs
  const paragraphs = document.querySelectorAll('p');
  
  paragraphs.forEach(p => {
    const text = p.innerHTML;
    // Look for margin note pattern
    const mnPattern = /\[MN\](.*?)\[\/MN\]/g;
    
    if (mnPattern.test(text)) {
      let newText = text;
      let count = 0;
      
      // Replace each margin note pattern
      newText = text.replace(mnPattern, (match, content) => {
        const id = `marginnote-${Math.random().toString(36).substring(2, 9)}`;
        count++;
        
        return `<label for="${id}" class="margin-toggle">⊕</label>
                <input type="checkbox" id="${id}" class="margin-toggle">
                <span class="marginnote">${content}</span>`;
      });
      
      p.innerHTML = newText;
    }
  });
}

/**
 * Process elements that should be full width (tables, wide images, etc.)
 */
function processFullWidthElements() {
  // Find all elements with full-width class
  const fullWidthElements = document.querySelectorAll('.full-width, .fullwidth');
  
  fullWidthElements.forEach(el => {
    // Ensure the element is wrapped properly
    if (!el.parentNode.classList.contains('fullwidth')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'fullwidth';
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);
    }
  });
  
  // Also look for [FULL] attribute on elements
  document.querySelectorAll('[data-full], [data-fullwidth]').forEach(el => {
    if (!el.parentNode.classList.contains('fullwidth')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'fullwidth';
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);
    }
  });
}

/**
 * Enhance figures with Tufte styling
 */
function processFigures() {
  // Find all images not already in figures
  const images = document.querySelectorAll('img:not(figure img)');
  
  images.forEach(img => {
    // Don't process icons or small images
    if (img.width < 100 || img.height < 100) return;
    
    // Create figure and figcaption elements
    const figure = document.createElement('figure');
    img.parentNode.insertBefore(figure, img);
    figure.appendChild(img);
    
    // If the image has alt text, use it as a caption
    if (img.alt && !img.alt.startsWith('_')) {
      const figcaption = document.createElement('figcaption');
      figcaption.textContent = img.alt;
      figure.appendChild(figcaption);
    }
    
    // If the image has a title attribute, use it as a margin note
    if (img.title) {
      const id = `img-note-${Math.random().toString(36).substring(2, 9)}`;
      
      const toggle = document.createElement('label');
      toggle.setAttribute('for', id);
      toggle.className = 'margin-toggle';
      toggle.textContent = '⊕';
      
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.id = id;
      checkbox.className = 'margin-toggle';
      
      const note = document.createElement('span');
      note.className = 'marginnote';
      note.innerHTML = img.title;
      
      figure.appendChild(toggle);
      figure.appendChild(checkbox);
      figure.appendChild(note);
    }
  });
}

/**
 * Add captions to tables based on titles
 */
function processTableCaptions() {
  // Find all tables
  const tables = document.querySelectorAll('table');
  
  tables.forEach(table => {
    // Skip tables that already have captions
    if (table.querySelector('caption')) return;
    
    // Check if the previous element is a paragraph that looks like a caption
    const prevEl = table.previousElementSibling;
    
    if (prevEl && prevEl.tagName === 'P' && prevEl.textContent.startsWith('Table:')) {
      const caption = document.createElement('caption');
      caption.innerHTML = prevEl.innerHTML.replace(/^Table:\s*/i, '');
      
      // If the table already has a caption element, replace it
      const existingCaption = table.querySelector('caption');
      if (existingCaption) {
        table.replaceChild(caption, existingCaption);
      } else {
        // Otherwise, add the caption to the table
        table.insertBefore(caption, table.firstChild);
      }
      
      // Remove the original caption paragraph
      prevEl.remove();
    }
  });
}

/**
 * Process special blockquote types
 */
function processBlockquotes() {
  const blockquotes = document.querySelectorAll('blockquote');
  
  blockquotes.forEach(blockquote => {
    // Process attribution style blockquotes
    const paragraphs = blockquote.querySelectorAll('p');
    const lastP = paragraphs[paragraphs.length - 1];
    
    if (lastP && lastP.textContent.startsWith('—')) {
      lastP.classList.add('attribution');
      lastP.style.textAlign = 'right';
      lastP.style.marginTop = '0.5rem';
    }
    
    // Process epigraph style blockquotes
    if (blockquote.classList.contains('epigraph') || 
        (blockquote.parentElement && blockquote.parentElement.classList.contains('epigraph'))) {
      if (!blockquote.parentElement.classList.contains('epigraph')) {
        const wrapper = document.createElement('div');
        wrapper.className = 'epigraph';
        blockquote.parentNode.insertBefore(wrapper, blockquote);
        wrapper.appendChild(blockquote);
      }
    }
    
    // Process note/tip/important blockquotes
    if (blockquote.classList.contains('note') || 
        blockquote.classList.contains('tip') || 
        blockquote.classList.contains('important')) {
      // Nothing more to do as CSS handles these
    }
  });
}

/**
 * Utility function to create a sidenote from content
 */
function createSidenote(content, index) {
  const id = `sidenote-${index}`;
  
  return `<label for="${id}" class="margin-toggle sidenote-number">${index}</label>
          <input type="checkbox" id="${id}" class="margin-toggle">
          <span class="sidenote">${content}</span>`;
}

/**
 * Utility function to create a margin note from content
 */
function createMarginNote(content, label = '⊕') {
  const id = `marginnote-${Math.random().toString(36).substring(2, 9)}`;
  
  return `<label for="${id}" class="margin-toggle">${label}</label>
          <input type="checkbox" id="${id}" class="margin-toggle">
          <span class="marginnote">${content}</span>`;
}