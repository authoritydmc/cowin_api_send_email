function populateDistricts(state_id) {
  var distDiv=document.getElementById('insrtDist');
  distDiv.innerHTML="";

  console.log("state_ID->",state_id);
  var url =
    "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" +
    String(state_id);

    var opt = document.createElement("option");

    opt.value = "0";
    opt.innerHTML = "Select Districts";
    // opt.setAttribute('disabled','disabled');
    distDiv.appendChild(opt);    
    console.log(distDiv.innerHTML);

  fetch(url)
    .then((response) => response.json()) // convert to json
    .then((json) => {
      var dis = json.districts;
      console.log(json.districts);
      for (var i = 0; i < dis.length; i++) {
        var option = document.createElement("option");

        option.value = dis[i].district_id;
        option.innerHTML = dis[i].district_name;

        distDiv.appendChild(option);
      }
    })
    .catch((err) => console.log("Request Failed", err)); // Catch errors
   

  }

function changedDistrict() {

  var districts = document.querySelector("#insrtDist");
  console.log(
    "Selected District->" +
      districts[districts.selectedIndex].text +
      " id=" +
      districts.value
  );
  if (districts.value!=0)
  {document.getElementById("dist_id").value = districts.value;
  document.getElementById("dist_name").value =districts[districts.selectedIndex].text;
  }
  else { document.getElementById("dist_id").value='';
  document.getElementById("dist_name").value='';
 }   
}


function selectBy_F(n)
{
  console.log("Selectby->"+n);

 

  if (n==0)
  {
    // show pincode ,Hide Dist
    $('#pinINs').show();
    $('.select').hide();
    $('.selectdiv').hide();

    
    
  }else
  {
    $('#pinINs').hide();
    $('.select').show();
    $('.selectdiv').show();



  }
}

// selectBy(0);

window.onload = function(){
  selectBy_F(1);
}
