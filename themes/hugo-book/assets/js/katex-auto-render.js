window.addEventListener("load", () => {
  const mathElements = document.querySelectorAll(".js-katex,.js-katex-display");

  for (let element of mathElements) {
    katex.render(element.textContent, element, {
      displayMode: element.classList.contains("js-katex-display"),
      throwOnError: false,
    });
  }
});
