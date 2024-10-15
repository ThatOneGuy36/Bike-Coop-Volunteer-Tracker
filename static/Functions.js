// When the user clicks the 'add student' button, make the form appear and disable the other buttons
function addVolunteer(){
	document.getElementById("addForm").removeAttribute("hidden");
	document.getElementById("deleteVolunteer").disabled = true;
	//document.getElementById("updateVolunteer").disabled = true;
}

// When the user clicks the 'delete student' button, make the form appear and disable the other buttons
function deleteVolunteer(){
	document.getElementById("deleteForm").removeAttribute("hidden");
	document.getElementById("addVolunteer").disabled = true;
	//document.getElementById("updateVolunteer").disabled = true;
}

// When the user clicks the 'update student' button, make the form appear and disable the other buttons
function updateVolunteer(){
	document.getElementById("updateForm").removeAttribute("hidden");
	document.getElementById("addVolunteer").disabled = true;
	document.getElementById("deleteVolunteer").disabled = true;
}

function printRewards(){
	document.getElementById("addVolunteer").disabled = true;
	//document.getElementById("updateVolunteer").disabled = true;
	document.getElementById("deleteVolunteer").disabled = true;
}



window.onload = function(){
    document.getElementById("addVolunteer").addEventListener("click", function(){
		addVolunteer();
	});
	
	document.getElementById("deleteVolunteer").addEventListener("click", function(){
		deleteVolunteer();
	});
	
	
	
	var slider = document.getElementById("myRange");
	var output = document.getElementById("rangeVal");
	output.innerHTML = slider.value; // Display the default slider value
	
	// Update the current slider value (each time you drag the slider handle)
	slider.oninput = function() {
		output.innerHTML = this.value;
	}
	
	
	// HANDLES THE REDEEM BUTTON FUNCTIONALITY
	var redeemButtons = document.querySelectorAll('.rewardRedeemButton');
	redeemButtons.forEach(function(button) {
		button.addEventListener('click', function() {
			var volunteerID = this.closest('tr').querySelector('#vID').textContent;
			var rewardName = this.previousSibling.textContent;
				
			// This might be an issue, since I want to get rid of numbers so that I don't have the quantity of product in the string,
			// but that means none of the reward names can have numbers in them
			rewardName = rewardName.replace(/[^a-zA-Z/? ]/g, '').trim();
		
			document.getElementById('volunteerIdInput').value = volunteerID;
			document.getElementById('rewardNameInput').value = rewardName;
			document.getElementById('updateHiddenForm').submit();
		});
	});
	
	
	
	// HANDLES THE PRINT VIEW BUTTON FUNCTIONALITY
	var printViewButtons = document.querySelectorAll('.printViewButton');
	
	printViewButtons.forEach(function(button) {
		button.addEventListener('click', function() {
			var volunteerID = this.closest('tr').querySelector('#vID').textContent;
		
			document.getElementById('volunteerIdInputPrint').value = volunteerID;
			document.getElementById('printForm').submit();
		});
	});
	
	
	
	// HANDLES THE PRINT VIEW BUTTON FUNCTIONALITY
	var updateHoursButtons = document.querySelectorAll('.updateHoursButton');
	
	updateHoursButtons.forEach(function(button) {
		button.addEventListener('click', function() {
			var volunteerID = this.closest('tr').querySelector('#vID').textContent;
		
			document.getElementById('VolunteerID_update_hours').value = volunteerID;
			
			updateVolunteer();
		});
	});
	
	
	// HANDLES THE EDIT NAME BUTTON FUNCTIONALITY
	var updateNameButtons = document.querySelectorAll('.editNameButton');
	
	updateNameButtons.forEach(function(button) {
		button.addEventListener('click', function() {
			var volunteerID = this.closest('tr').querySelector('#vID').textContent;
		
			document.getElementById('VolunteerID_update_name').value = volunteerID;
			document.getElementById("updateForm_name").removeAttribute("hidden");
			
			document.getElementById("addVolunteer").disabled = true;
			document.getElementById("deleteVolunteer").disabled = true;
		});
	});
	
	
	// HANDLES THE EDIT STUDENT STATUS BUTTON FUNCTIONALITY
	var updateStatusButtons = document.querySelectorAll('.editStudentButton');
	
	updateStatusButtons.forEach(function(button) {
		button.addEventListener('click', function() {
			var volunteerID = this.closest('tr').querySelector('#vID').textContent;
		
			document.getElementById('VolunteerID_update_status').value = volunteerID;
			document.getElementById("updateForm_student").removeAttribute("hidden");
			
			document.getElementById("addVolunteer").disabled = true;
			document.getElementById("deleteVolunteer").disabled = true;
		});
	});
}