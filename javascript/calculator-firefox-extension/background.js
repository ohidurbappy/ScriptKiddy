function resetDefaultSuggestion() {
    browser.omnibox.setDefaultSuggestion({
      description:'Super Calculator'
    });
  }


  function evil(fn) {
    return new Function('return ' + fn)();
  }
  
  resetDefaultSuggestion();

browser.omnibox.onInputCancelled.addListener(function() {
    resetDefaultSuggestion();
  });

  

// Update the suggestions whenever the input is changed.
browser.omnibox.onInputChanged.addListener((text, addSuggestions) => {
    browser.omnibox.SuggestResult({'description': evil(text)});
    alert(text)
});



// Open the page based on how the user clicks on a suggestion.
browser.omnibox.onInputEntered.addListener((text, disposition) => {
    // browser.navigate(text)

  });


