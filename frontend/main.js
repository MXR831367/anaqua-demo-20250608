window.addEventListener("DOMContentLoaded", (event) => {
  getVisitCount();
});

const functionApi =
  "https://anaqua-20250107demo.azurewebsites.net/api/count?id=3";

const getVisitCount = () => {
  let count = 37;
  console.log("getVisitCount started.");
  fetch(functionApi)
    .then((response) => {
      return response.json();
    })
    .then((response) => {
      console.log("Website called function API.");
      count = response.count;
      document.getElementsByClassName(
        "countertext"
      )[0].innerText = `VIEWS: ${count}`;
    })
    .catch(function (error) {
      console.log(error);
    });
  return count;
};
