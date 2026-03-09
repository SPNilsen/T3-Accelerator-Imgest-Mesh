document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll(".caption").forEach(function(caption){
    let html = caption.innerHTML;
    // Find the first colon in the caption
    let colonIndex = html.indexOf(':');
    if (colonIndex !== -1) {
      // Get the label text up to (but not including) the colon, then trim extra space
      let label = html.slice(0, colonIndex).trim();
      // Append a period instead of a colon
      let newLabel = label + ".";
      // Get the rest of the caption after the colon
      let rest = html.slice(colonIndex + 1);
      // Replace the caption HTML with the new label and the rest of the caption
      caption.innerHTML = '<span class="caption-label">' + newLabel + '</span>' + rest;
    }
  });
});
