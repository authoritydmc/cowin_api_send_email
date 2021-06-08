function refresh_page(){
  window.location.reload();
  console.log("Refreshing page");
}

var checkbox = document.querySelector("#show0Qty");

if(checkbox!=null){


checkbox.addEventListener("change", function () {
  if (this.checked) {
    Hide(true);
    hideCenter(true);
  } else {
    Hide(false);
    hideCenter(false);
  }
});
}
var dontHide = [];
function Hide(shdhide) {
  var allAvailableSpans = document.getElementsByClassName("available");
  for (let i = 0; i < allAvailableSpans.length; i++) {
    if (allAvailableSpans[i].innerText == 0) {
      // console.log("Method is called at i "+i+" value->"+allAvailableSpans[i].innerText);
      if (shdhide == true) {
        allAvailableSpans[i].parentNode.style.display = "none";
        // hide this parents
      } else {
        allAvailableSpans[i].parentNode.style.display = "block";

        //show thier parent
      }
    } else {
      if (
        dontHide.includes(
          allAvailableSpans[i].parentNode.parentNode.parentNode.id
        ) == false
      )
        dontHide.push(allAvailableSpans[i].parentNode.parentNode.parentNode.id);
    }
  }
}

function hideCenter(hide) {
  var allcenters = document.getElementsByClassName("center-view");
  console.log("dont hide ->", dontHide);

  for (var x = 0; x < allcenters.length; x++) {

    if (dontHide.includes(allcenters[x].id) == false) {

      if (hide == true) {
        console.log("hiding center " + allcenters[x].id);
        allcenters[x].style.display = "none";
      } else {
        console.log("showing center " + allcenters[x].id);
        allcenters[x].style.display = "block";
      }

    }else
    {
        console.log("dont hide center matched at " + allcenters[x].id);

    }
  }
}
