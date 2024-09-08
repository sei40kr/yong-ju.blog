function handler(event) {
  var request = event.request;
  var uri = request.uri;

  if (uri === "/") {
    request.uri = "/page/1/index.html";
  }
  // Check whether the URI is missing a file name.
  else if (uri.endsWith("/")) {
    request.uri += "index.html";
  }
  // Check whether the URI is missing a file extension.
  else if (!uri.includes(".")) {
    request.uri += "/index.html";
  }

  return request;
}
