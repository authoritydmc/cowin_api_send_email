// alert("Update USer js called")
var hideVal_pincode=0;
var hideVal_dist=1;
console.log("Welcoming User")

function fetchUserData(){
    var oldselectBy=$("#old_selectby").val();
    var olddistId=$("#old_dist_id").val();
    console.log(olddistId);
    console.log(oldselectBy);

    if(oldselectBy=="pincode")
    {
        // user previously has pincode based selection
        selectBy_F(hideVal_pincode);

    }else{
        selectBy_F(hideVal_dist);

        // now select the State which is selected

    }


}

fetchUserData();


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
      $('#state_list').hide();

      
  
      
      
    }else
    {
      $('#pinINs').hide();
      $('.select').show();
      // $('.selectdiv').show();
      $('#state_list').show();

  
  
  
    }
  }

  
  
const inputField = document.querySelector('.chosen-value');
const dropdown = document.querySelector('.value-list');
const dropdownArray = [...document.querySelectorAll('li')];
console.log(typeof dropdownArray);
dropdown.classList.add('close');

let valueArray = [];
dropdownArray.forEach(item => {
  valueArray.push(item.textContent);
});

const closeDropdown = () => {
  dropdown.classList.remove('open');
};

inputField.addEventListener('input', () => {
  dropdown.classList.add('open');
  let inputValue = inputField.value.toLowerCase();
  let valueSubstring;
  if (inputValue.length > 0) {
    for (let j = 0; j < valueArray.length; j++) {if (window.CP.shouldStopExecution(0)) break;
      if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
        dropdownArray[j].classList.add('closed');
      } else {
        dropdownArray[j].classList.remove('closed');
      }
    }window.CP.exitedLoop(0);
  } else {
    for (let i = 0; i < dropdownArray.length; i++) {if (window.CP.shouldStopExecution(1)) break;
      dropdownArray[i].classList.remove('closed');
    }window.CP.exitedLoop(1);
  }
});

dropdownArray.forEach(item => {
  item.addEventListener('click', evt => {
    inputField.value = item.textContent;
    dropdownArray.forEach(dropdown => {
      dropdown.classList.add('closed');
    });
  });
});

inputField.addEventListener('focus', () => {
  inputField.placeholder = 'Type to filter';
  dropdown.classList.add('open');
  dropdownArray.forEach(dropdown => {
    dropdown.classList.remove('closed');
  });
});

inputField.addEventListener('blur', () => {
  inputField.placeholder = 'Select State';
  dropdown.classList.remove('open');
});

document.addEventListener('click', evt => {
  const isDropdown = dropdown.contains(evt.target);
  const isInput = inputField.contains(evt.target);
  if (!isDropdown && !isInput) {
    dropdown.classList.remove('open');
  }
});