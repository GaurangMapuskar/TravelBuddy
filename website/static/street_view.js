// static/js/street_view.js
function showStreetView() {
  var location = document.getElementById("locationInput").value;
  var api_key = "AIzaSyD9WjAqdTHoQGaUlP9dgXr7qlzpnfAGJ98"; // Replace with your actual API key

  fetch("/get_coordinates", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ location: location }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error_message) {
        document.getElementById(
          "street-view-container"
        ).innerHTML = `<p style="color: red;">${data.error_message}</p>`;
      } else {
        var streetViewUrl = `https://www.google.com/maps/embed/v1/streetview?location=${data.latitude},${data.longitude}&key=${api_key}`;
        document.getElementById("street-view-container").innerHTML = `
                <h2>Street View for Location: ${location}</h2>
                <iframe width="100%" height="400" frameborder="0" style="border:0" src="${streetViewUrl}" allowfullscreen></iframe>
            `;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
