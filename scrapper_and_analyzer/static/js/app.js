// var getValue = document.getElementById("values");
// var but = document.getElementById("searchBut");
// // get element by name
// var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
// console.log(csrf);
// but.addEventListener("click", () => {
//   if (getValue.value == "") {
//     return;
//   } else {
//     sessionStorage.setItem(
//       "user",
//       JSON.stringify(getValue.value.toLowerCase())
//     );
//     // getValue.value = "";
//     // request to server and set the getValue to the server
//     $.ajax({
//       url: "http://localhost:8000/results",
//       type: "POST",
//       data: {
//         user: getValue.value.toLowerCase(),
//       },
//       success: function (data) {
//         console.log(data);
//         if (data.length == 0) {
//           alert("No result found!");
//         } else {
//           window.location.href = "./result.html";
//         }
//       },
//     });

//     changePage();
//   }
// });

// function changePage() {
//   window.location.href = "Results/results.html";
// }
