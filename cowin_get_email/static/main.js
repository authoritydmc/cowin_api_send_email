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
document.querySelector('#states').style.display="none"; 
document.querySelector('#districts').style.display="none";  
document.querySelector('#dist_name').style.display="none";  
document.querySelector('#dist_id').style.display="none";  

document.querySelector('#pincode').style.display="block"; 

document.querySelector('#pincode').required=true;


document.querySelector('#lblpin').style.display="block";  

document.querySelector('#lbldist').style.display="none";   
document.querySelector('#lblstates').style.display="none";   

document.querySelector('#dist_name').value=''; 
document.querySelector('#dist_id').value='';  




}else
{
  //select By dist

  document.querySelector('#states').style.display="block";  
document.querySelector('#districts').style.display="block";  
document.querySelector('#pincode').style.display="none"; 
document.querySelector('#dist_name').style.display="none"; 
document.querySelector('#dist_id').style.display="none"; 
document.querySelector('#lblpin').style.display="none";   
document.querySelector('#pincode').value='';

document.querySelector('#lbldist').style.display="block";  
document.querySelector('#lblstates').style.display="block"; 
document.querySelector('#pincode').required=false;


}


}

selectBy(0);
