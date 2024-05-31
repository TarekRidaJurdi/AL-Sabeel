
// Show closeButton when checked and hide it when unchecked: 

// Get all checkboxes
let checkboxes = document.querySelectorAll(".checkbox-f");

// Add click event listener to each checkbox
checkboxes.forEach(checkbox => {

  checkbox.addEventListener("click", () => {

    // Get the corresponding label as a child of checkbox
    let label = checkbox.nextElementSibling;

    // Toggle the display of the close button as a child of label based on the checkbox state
    label.querySelector(".close-button").style.display = checkbox.checked ? "inline" : "none";
  });
});
 

// Form with Multiple Steps 
var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "flex";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "حفظ";
  } else {
    document.getElementById("nextBtn").innerHTML = "التالي";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {

    // Call generate report function when reach the submit stage
    // generateReport();

    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
   
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    
    // If a field is empty or a radio/checkbox is not selected...
    if ( y[i].value == "" && !y[i].checked) {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
  //The space between the double quotes and the word "active" is important because it ensures that there is a space between the existing class names in the className property and the new class name being added. The += operator is used to concatenate the existing class names with the new class name
}


// Generate report based on form input data

function generateReport() {
  // Collect data from form fields
  var husband = document.getElementById('husband').value;
  var father = document.getElementById('father').value;
  var family = document.getElementById('family').value;
  var birthday = document.getElementById('birthday').value;
  var nationalNum = document.getElementById('nationalNum').value;
  var job = document.getElementById('job').value;
  var wife = document.getElementById('wife').value;
  var fatherW = document.getElementById('father-w').value;
  var familyW = document.getElementById('family-w').value;
  var birthdayW = document.getElementById('birthday-w').value;
  var nationalNumW = document.getElementById('nationalNum-w').value;
  var jobW = document.getElementById('job-w').value;
  var firstChild = document.getElementById('first-child').value;
  var birthdayChild = document.getElementById('birthday-child').value;
  var studyWork = document.getElementById('study-work').value;
  var notes = document.getElementById('notes').value;
  var state = document.getElementById('state').value;
  var city = document.getElementById('city').value;
  var village = document.getElementById('village').value;
  var specificPoint = document.getElementById('specificPoint').value;
  var own = document.getElementById('own').value;
  var rent = document.getElementById('rent').value;
  var temporary = document.getElementById('temporary').value;
  var familyHealth = document.getElementById('familyHealth').value;
  var additionalInfo = document.getElementById('additionalInfo').value;
  var basicMobile = document.getElementById('basicMobile').value;
  var alternativeMobile = document.getElementById('alternativeMobile').value;
  var telephone = document.getElementById('telephone').value;
  var statusSource = document.getElementById('statusSource').value;
  var regDate = document.getElementById('regDate').value;
  var applicant = document.getElementById('applicant').value;
  var dataEntrier = document.getElementById('dataEntrier').value;
  var applicantEvaluation = document.getElementById('applicantEvaluation').value;
  var evaluationText = document.getElementById('evaluationText').value;
  var managementNotes = document.getElementById('managementNotes').value;

  // Display buttons after generating the report 
  document.getElementById('modify').style.display = 'block';
  document.getElementById('archive').style.display = 'block';
  document.getElementById('assistRecord').style.display = 'block';

  // Create the report content
  var reportContent = `
  <h5 class="label-style">العائلة:</h5>
  <div class="row pb-5">
    <div class="col-md-3 col-lg-2">
      <p> ${husband} ${father}
      ${family}</p>
    </div>
    <div class="col-md-3 col-lg-2"> 
    <p> ${birthday} </p>
    </div>
    <div class="col-md-3 col-lg-2"> 
    <p> ${nationalNum} </p>
    </div>
    <div class="col-md-3 col-lg-6 text-lg-center"> 
    <p> ${job} </p>
    </div>
    <div class="col-md-3 col-lg-2">
      <p> ${wife} ${fatherW}
      ${familyW}</p>
    </div>
    <div class="col-md-3 col-lg-2"> 
    <p> ${birthdayW} </p>
    </div>
    <div class="col-md-3 col-lg-2"> 
    <p> ${nationalNumW} </p>
    </div>
    <div class="col-md-3 col-lg-6 text-lg-center"> 
    <p> ${jobW} </p>
    </div>
    <div class="col-md-6 col-lg-2">
      <p> ${firstChild}</p>
    </div>
    <div class="col-md-6 col-lg-2"> 
    <p> ${birthdayChild} </p>
    </div>
    <div class="col-md-6 col-lg-2"> 
    <p> ${studyWork} </p>
    </div>
    <div class="col-md-6 col-lg-6"> 
    <p> ${notes} </p>
    </div>
    <h5 class="label-style">العنوان,الإقامةوالسكن:</h5>
    <div class="col-md-4 col-lg-12"> 
    <p> ${state},${city},${village} </p>
    </div>
    <div class="col-md-4 col-lg-12"> 
    <p> ${specificPoint} </p>
    </div>
    <!-- <div class="col-md-6 col-lg-12"> 
    <p>البيت: ${own} </p>
    </div>
    <div class="col-md-6 col-lg-12"> 
    <p>البيت: ${rent} </p>
    </div>
    <div class="col-md-6 col-lg-12"> 
    <p>البيت: ${temporary} </p>
    </div> -->
    <h5 class="label-style">الحالة الصحية:</h5>
    <div class="col-md-6 col-lg-12"> 
    <p> ${familyHealth} </p>
    </div>
    <h5 class="label-style"> معلومات إضافية:</h5>
    <div class="col-md-6 col-lg-12"> 
    <p> ${additionalInfo} </p>
    </div>
    <h5 class="label-style"> معلومات التواصل:</h5>
    <div class=" col-lg-12"> 
    <p> موبايل 1: ${basicMobile} </p>
    </div>
    <div class=" col-lg-12"> 
    <p> موبايل 2: ${alternativeMobile} </p>
    </div>
    <div class=" col-lg-12"> 
    <p>  ثابت  :${ telephone }  </p>
    </div>
    <h5 class="label-style">البيانات والإدخال:</h5>
    <div class=" col-lg-12"> 
    <p> مصدر الحالة: ${statusSource} </p>
    </div>
    <div class=" col-lg-12"> 
    <p> تاريخ التسجيل: ${regDate} </p>
    </div>
    <div class=" col-lg-12"> 
    <p>مقدم الطلب : ${applicant} </p>
    </div>
    <div class=" col-lg-12"> 
    <p> مدخل البيانات: ${dataEntrier} </p>
    </div>
    <h5 class="label-style"> تقييم مقدم الطلب:</h5>
    <div class="col-md-6 col-lg-12"> 
    <p> ${applicantEvaluation} </p>
    </div>
    <h5 class="label-style"> تقييم الدراسات :</h5>
    <div class="col-md-6 col-lg-12">
    <p>${evaluationText.replace(/\//g,':<br/>')}</p>
</div>
    <h5 class="label-style"> ملاحظات الإدارة:</h5>
    <div class="col-md-6 col-lg-12"> 
    <p> ${managementNotes} </p>
    </div>
    </div>
  `;

  // Display the report in the 'report' div
  document.getElementById('report').innerHTML = reportContent;
}

// Call the generateReport function when the 'Next' button is clicked
document.getElementById('Generate').addEventListener('click', function() {
  generateReport();});



 // Active Head Table

document.querySelectorAll(".table-page ul li").forEach(li => {

  li.addEventListener("click", (element) =>
  {   
      element.target.parentElement.querySelectorAll(".active").forEach(event => {
          // Remove active class 
          event.classList.remove("active")
         });
         //Add classlist to target element li
         element.target.classList.add("active");

     });
 });





