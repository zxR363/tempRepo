/*
*  Create a form that handles submit and reset.
*  You have free reign to decide what the form
*  will be for, but the information provided should
*  be shown back to the user in a read only fashion.
*  It should allow the user to repeatedly fill out
*  the form and appending the read only data to the
*  page.
*
*  Requirements:
*   -A <form> element with contained controls
*   -At least 5 form fields
*   -At least 3 types of form fields:
*     ~text input
*     ~email input
*     ~textarea
*     ~checkbox
*     ~radio button
*     ~slider
*     ~etc
*   -At least 3 fields with validation:
*     ~min/max number value
*     ~character count min/max
*     ~required field
*     ~regex pattern
*     ~etc
*   -Form fields should have labels
*   -A submit button
*   -On submit, inputs should be displayed read only
*     and form should be reset.
*   -A reset button that resets form fields
*   -At least 10 styles (color, font size, etc)
*
*  Please upload your HTML and JS files with your
*  submission along with your css file if you used one.
*/


// YOUR CODE STARTS HERE
function createDiv() {
	var iDiv = document.createElement('div');
	iDiv.id = 'block';
	iDiv.className = 'block';

	iDiv.style="background-color:#D3D3D3;padding: 35px;margin-top: 25px;margin-right: 25px;margin-bottom: 25px";
	//document.getElementsByTagName('body')[0].appendChild(iDiv);
	return iDiv
}

var elementful = document.createElement("ul");  
elementful.style="list-style-type:none";

document.getElementsByTagName('body')[0].appendChild(elementful);
document.getElementsByTagName('body')[0].style.marginLeft="25px";


//-------------------SUBMIT PLACE --------------------------

iDiv3 = createDiv();
iDiv3.style.marginLeft="38px";

var elementful2 = document.createElement("ul");  
elementful2.style="list-style-type:none;margin-left: -40px;";

const f = document.createElement("form");
f.id="newForm";
f.appendChild(elementful2);

iDiv3.appendChild(f);

//----------------------------------------------NAME----------------------------------------------
function createNameField(name,marginSize) {
	var t = document.createTextNode(name);
	//-----------INPUT------------------
	var input = document.createElement("input");
	input.type = "text";
	input.style.marginLeft=marginSize;
		
	//---------------------------
	var li = document.createElement("li");
	li.appendChild(t);
	li.appendChild(input);
	
	return li
}

var names = createNameField("Name :","44px");
var surnames = createNameField("Surname: ","26px");
names.style.marginBottom="5px";
surnames.style.marginBottom="5px";
elementful2.appendChild(names);
elementful2.appendChild(surnames);
//--------------------------------------------------------------------------------------
//----------------------------------------------EMAIL----------------------------------------------
function createEmail()
{
	var t = document.createTextNode("Email: ");
	
	//----Email
	var email = document.createElement('input');
	email.setAttribute('type', 'email');
	elementful2.appendChild(email);

	email.addEventListener("click", function () {
	  
	});
	email.style.marginLeft="44px";
	
	var li = document.createElement("li");
	li.appendChild(t);
	li.appendChild(email);
	
	return li
}
var mail = createEmail();
elementful2.appendChild(mail);

//--------------------------------------------------------------------------------------

//----Sub Header---
var h = document.createElement("H2"); 
var t = document.createTextNode("");
h.appendChild(t); 
elementful2.appendChild(h);

//----DETAIL ---------- 
var checkbox = document.createElement('input');
	checkbox.setAttribute('type', 'checkbox');
	
checkbox.addEventListener("click", function () {
	if(checkbox.checked)
	{
		textarea.disabled="true";
	}
	
});
		
var detail = document.createTextNode("Details:");
	
var li1 = document.createElement("li");
li1.appendChild(checkbox);
li1.appendChild(detail);

elementful2.appendChild(li1);

//---------Text Area---
var hc = document.createElement("H1");

var textarea = document.createElement("textarea");
textarea.style="margin-left: 20px;margin-top:-20px";
textarea.rows=4;
textarea.cols=50;

elementful2.appendChild(hc);
elementful2.appendChild(textarea);

//---------------------------BUTTONS-----------------------
let btn = document.createElement("button");
btn.innerHTML = "Submit";
btn.style.background='#C71585';
btn.style.color='#ffffff';
btn.addEventListener("click", function () {
	
});

let resetBtn = document.createElement("button");
resetBtn.innerHTML = "Reset";
resetBtn.style.background='#C71585';
resetBtn.style.color='#ffffff';
resetBtn.style.marginLeft="15px";
resetBtn.addEventListener("click", function () {
	f.reset();	
});

var liBtn = document.createElement("li");
liBtn.appendChild(btn);
liBtn.appendChild(resetBtn);
liBtn.style.marginTop="5px";

elementful2.appendChild(liBtn);


document.getElementsByTagName('body')[0].appendChild(iDiv3);

// YOUR CODE ENDS HERE
