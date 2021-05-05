function populateDistricts() {
  var state_id = document.querySelector("#states");
  var dist_DOM = document.getElementById("districts");
  var opt = document.createElement("option");

  dist_DOM.innerHTML = "";
  opt.value = "0";
  opt.innerHTML = "Select Districts";
  dist_DOM.appendChild(opt);

  console.log(state_id.value);
  var url =
    "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" +
    String(state_id.value);

  // GET Request.
  fetch(url)
    .then((response) => response.json()) // convert to json
    .then((json) => {
      var dis = json.districts;
      console.log(json.districts);
      for (var i = 0; i < dis.length; i++) {
        var option = document.createElement("option");

        option.value = dis[i].district_id;
        option.innerHTML = dis[i].district_name;

        dist_DOM.appendChild(option);
      }
    })
    .catch((err) => console.log("Request Failed", err)); // Catch errors
}

function changedDistrict() {
  var districts = document.querySelector("#districts");
  console.log(
    "Selected District->" +
      districts[districts.selectedIndex].text +
      " id=" +
      districts.value
  );
  document.getElementById("dist_id").value = districts.value;
  document.getElementById("dist_name").value =
    districts[districts.selectedIndex].text;
}

function selectBy(val)
{
if(val==0)
{
  // select By pincode
document.querySelector('#states').style.visibility="hidden";  
document.querySelector('#districts').style.visibility="hidden";  
document.querySelector('#dist_name').style.visibility="hidden";  
document.querySelector('#dist_id').style.visibility="hidden";  

document.querySelector('#pincode').style.visibility='visible';

document.querySelector('#lblpin').style.visibility="visible";  

document.querySelector('#lbldist').style.visibility="hidden";  
document.querySelector('#lblstates').style.visibility="hidden";  




}else
{
  //select By dist

  document.querySelector('#states').style.visibility="visible";  
document.querySelector('#districts').style.visibility="visible";  
document.querySelector('#pincode').style.visibility='hidden';
document.querySelector('#dist_name').style.visibility="visible";  
document.querySelector('#dist_id').style.visibility="visible";
document.querySelector('#lblpin').style.visibility="hidden";  

document.querySelector('#lbldist').style.visibility="visible";  
document.querySelector('#lblstates').style.visibility="visible"; 

}


}

selectBy(0);
