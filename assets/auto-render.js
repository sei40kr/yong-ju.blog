const mathElements = document.getElementsByClassName("js-katex");
const displayMathElements = document.getElementsByClassName("js-katex-display");

for (let element of mathElements) {
  katex.render(element.textContent, element);
}
for (let element of displayMathElements) {
  katex.render(element.textContent, element, { displayMode: true });
}
