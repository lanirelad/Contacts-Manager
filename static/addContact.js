// declarations
let nameTextBoxID = "name";
let nameTBlabel = "nameLabel";
let profileImageID = "profileImg";
let elementNameTB = document.getElementById(nameTextBoxID);
let elementNameL = document.getElementById(nameTBlabel);
let tbOrgTextColor = elementNameTB.style.color;
let emptyCheckboxBG = "red";
let checkedCheckboxBG = "green";
let uncheckedCheckboxBG = "white";
let checkboxContainer = "CBcontainer";
let checkboxID = "iAgree";
let CBcontainerList = document.getElementsByClassName(checkboxContainer);
let elementCBbackground = CBcontainerList[0];
let elementCB = document.getElementById(checkboxID);
let elementProfileImage = document.getElementById(profileImageID);
let popup = document.getElementById('popup');
let termsContent = document.getElementById('termsContent');
let okButton = document.getElementById('okButton');
let elementContExist = document.getElementById('contExist');
let elementForm = document.getElementById('addForm')
// ---------


elementNameTB.onfocus = () => elementNameL.style.fontWeight = "900"; // make 'name' label bolder on focus
elementNameTB.onblur = lostFocus; // assign event listener for 'name' textbox
elementProfileImage.onchange = function() {profileImgValidation(this)}; // assign validation to image upload

// name textbox manipulating
function lostFocus()
{
	elementNameL.style.fontWeight = "normal";
	if (elementNameTB.value.trim() !== "")
		{
			elementNameTB.style.color = "MediumSeaGreen";
		}
	else
		{
			elementNameTB.style.color = tbOrgTextColor;
		}
}

// checkbox manipulating
elementCBbackground.style.backgroundColor = "tomato";
elementCB.addEventListener('change', () => 
	{
		if (elementCB.checked)
			{
				popup.style.display = 'block';
				termsContent.innerHTML = `<p>Greetings, intrepid voyager, and prepare to embark on a perilous journey through the tangled jungles of Legal Limbo!<br>
										By stepping foot into this digital domain or availing yourself of its enigmatic services, you unwittingly subject yourself to the whims of fate and the follies of code.<br>
										Steel yourself, for the path ahead is fraught with danger, despair, and the occasional cat picture.</p>
										<p><b>Preamble of Peril</b>: Behold, the gateway to our digital odyssey! Know ye that traversing this realm demands the fortitude of a thousand sysadmins and the resilience of a rubber duck.
										Brace yourself for the trials that lie ahead, for every line of code is a potential minefield, and every bug a beast waiting to rear its ugly head.</p>
				
										<p><b>Declaration of Debugging</b>: Prepare to do battle with the dreaded bugs, those elusive creatures that lurk in the darkest corners of the codebase.<br>
										With every line of code you write, remember that a bug lies in wait, ready to strike when you least expect it.<br>
										But fear not, brave soul, for with every bug squashed comes the sweet taste of victory and the promise of a brighter tomorrow.</p>
				
										<p><b>Dependencies of Despair</b>: Enter the labyrinth of dependencies at your own peril, for therein lies a tangled web of version conflicts and broken builds.<br>
										Beware the siren song of the latest and greatest libraries, for they may lead you astray and leave you stranded in dependency hell.<br>
										And remember, dear traveler, that for every dependency resolved, there's another waiting to take its place.</p>
				
										<p><b>Privacy in Peril</b>: Guard your personal information like a dragon hoards treasure, for in the realm of cyberspace, data is the currency of the realm.<br>
										Beware the prying eyes of hackers and data thieves, for they lurk in the shadows, waiting to pounce on the unwary and plunder their digital riches.</p>
				
										<p><b>Code of Catastrophe</b>: Abandon hope, all ye who enter here, for the path of the programmer is fraught with peril and frustration.<br>
										Brace yourself for the trials of bad indentation, spaghetti code, and runtime errors galore.<br>
										But fear not, for in the fires of adversity, true programmers are forged, their resolve as unyielding as their code is unbreakable.</p>
				
										<p><b>Exceptional Errors</b>: Prepare for the inevitable onslaught of exceptions, those fiendish foes that lie in wait to thwart your every move.<br>
										From null pointer exceptions to out-of-memory errors, they come in all shapes and sizes, each more insidious than the last.<br>
										But fear not, for with every exception comes an opportunity to learn and grow, to become the master of your own digital destiny.</p>
				
										<p><b>Acknowledgment of Adversity</b>: And so, dear traveler, we bid you farewell as you embark on this perilous journey through the digital wilderness.<br>
										May your code be bug-free, your dependencies up-to-date, and your resolve unshakable in the face of adversity.<br>
										For in this chaotic world of ones and zeros, only the bold and the brave shall emerge victorious!</p>`;
				
			}
		else
			{
				popup.style.display = 'none';
				elementCBbackground.style.backgroundColor = 'tomato';
			}
	});


// validate profile image is png only!
function profileImgValidation(input)
{
	const file = input.files[0];
    const fileType = file.type.toLowerCase();
    if (fileType !== 'image/png') 
		{
        alert('Please select a PNG file.');
        input.value = '';
    	}

	var reader = new FileReader();
    reader.onload = function(e) {
        var thumbnailContainer = document.getElementById("thumbnailContainer");
        thumbnailContainer.innerHTML = ""; // clear previous thumbnail if exists

        var thumbnail = document.createElement("img");
        thumbnail.src = e.target.result;
        thumbnail.width = 100; // adjust thumbnail size as needed
        thumbnailContainer.appendChild(thumbnail);
    }

    reader.readAsDataURL(file);
}


document.addEventListener("DOMContentLoaded", function() 
{
	//elementContExist.style.display = 'none'; defined in css for a smoother faster reaction
	termsContent.addEventListener('scroll', function() 
	{
	  if (this.scrollTop + this.clientHeight >= this.scrollHeight) 
		{
			okButton.disabled = false;
		} 
	  else 
		{
			okButton.disabled = true;
		}
	});
  
	okButton.addEventListener('click', function() 
	{
		elementCB.checked = true;
		elementCBbackground.style.backgroundColor = 'transparent';
	  	popup.style.display = 'none';
	});

});





// house keeping

// window.onload = function() 
// {
//     const fileInput = document.getElementById('profileImg');
//     const thumbnail = document.getElementById('thumbnailContainer');

//     // Get the top position of the file input
//     const fileInputPosition = fileInput.getBoundingClientRect();
//     const fileInputTop = fileInputPosition.top + window.scrollY;

//     // Set the top position of the thumbnail to match the file input
//     thumbnail.style.top = fileInputTop + 'px';
// };


// // Function to display the thumbnail when a file is selected
// fileInput.addEventListener("change", function(event)
// {
// 	const file = event.target.files[0];
// 	const reader = new FileReader();

// 	reader.onload = function(e) 
// 	{
// 		thumbnailImg.src = e.target.result;
// 	};

// 	reader.readAsDataURL(file);

// 	// Append the thumbnail image to the thumbnail container
// 	thumbnailContainer.appendChild(thumbnailImg);
// });