// Text Selection Utility for RAG Chatbot Integration
// Provides functionality to capture selected text on the page

class TextSelectionUtil {
  // Get the currently selected text on the page
  static getSelectedText() {
    const selection = window.getSelection();
    if (selection && selection.rangeCount > 0) {
      return selection.toString().trim();
    }
    return '';
  }

  // Get the range of the current selection
  static getSelectionRange() {
    const selection = window.getSelection();
    if (selection && selection.rangeCount > 0) {
      return selection.getRangeAt(0);
    }
    return null;
  }

  // Highlight selected text temporarily (for UI feedback)
  static highlightSelection() {
    const range = this.getSelectionRange();
    if (range) {
      const span = document.createElement('span');
      span.style.backgroundColor = 'yellow';
      span.style.opacity = '0.3';
      range.surroundContents(span);

      // Remove highlight after a short time
      setTimeout(() => {
        if (span.parentNode) {
          const parent = span.parentNode;
          const textNode = document.createTextNode(span.textContent);
          parent.replaceChild(textNode, span);
        }
      }, 500);
    }
  }

  // Check if text is currently selected
  static isTextSelected() {
    const selectedText = this.getSelectedText();
    return selectedText.length > 0;
  }

  // Get contextual information about the selected text
  static getSelectionContext() {
    const selectedText = this.getSelectedText();
    if (!selectedText) {
      return null;
    }

    const range = this.getSelectionRange();
    const context = {
      text: selectedText,
      length: selectedText.length,
      rect: range ? range.getBoundingClientRect() : null,
      element: range ? range.startContainer.parentElement : null
    };

    return context;
  }
}

// Export the text selection utility
export default TextSelectionUtil;