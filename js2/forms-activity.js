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
function createNameField(customId,name,marginSize) {
	var t = document.createTextNode(name);
	//-----------INPUT------------------
	var input = document.createElement("input");
	input.id=customId;
	input.type = "text";
	input.required =true;
	input.setAttribute("minlength", "2");
	input.setAttribute('pattern',"[A-Za-z0-9]{2,}");
	input.setAttribute('title',"Must contain at least 2 character");
	input.style.marginLeft=marginSize;

	//---------------------------
	var li = document.createElement("li");
	li.appendChild(t);
	li.appendChild(input);
	
	return li
}

var names = createNameField("name","Name :","44px");
var surnames = createNameField("surname","Surname: ","26px");
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
	email.id="mail";
	email.required=true;
	email.setAttribute('type', 'email');
	email.setAttribute('pattern',"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$");
	email.setAttribute('title',"Must contain at least 2 after @x. character");
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
checkbox.id ="chc";
checkbox.setAttribute('type', 'checkbox');

checkbox.addEventListener("change", function () {
	
	if(document.getElementById("chc").checked)
	{
		textarea.removeAttribute('disabled');
	}
	else
	{
		textarea.setAttribute('disabled','disabled');
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
textarea.id="abc";
textarea.style="margin-left: 20px;margin-top:-20px";
textarea.rows=4;
textarea.cols=50;
textarea.disabled="true";

elementful2.appendChild(hc);
elementful2.appendChild(textarea);

function createResult(valName,valSur,valMail,valDescription) {
	var nm = document.createTextNode("Name:"+valName);
	var srname = document.createTextNode("Surname:"+valSur);
	var mail = document.createTextNode("eMail:"+valMail);
	var txtarea = document.createTextNode("description:"+valDescription);
	
	var v = document.createElement("ul"); 
	var p1 = document.createElement("li");
	var p2 = document.createElement("li");
	var p3 = document.createElement("li");
	var p4 = document.createElement("li");
	p1.appendChild(nm);
	v.appendChild(p1);
	p2.appendChild(srname);
	v.appendChild(p2);
	p3.appendChild(mail);
	v.appendChild(p3);
	p4.appendChild(txtarea);
	v.appendChild(p4);
	
	return v
}


//---------------------------BUTTONS-----------------------


var val;
let btn = document.createElement("button");
btn.type="button";
btn.innerHTML = "Submit";
btn.style.background='#C71585';
btn.style.color='#ffffff';
btn.addEventListener("click", function () {
	iDiv2 = createDiv();
	iDiv2.style.marginLeft="38px";
	val = createResult(document.getElementById('name').value,document.getElementById('surname').value,document.getElementById('mail').value,document.getElementById('abc').value);
	iDiv2.appendChild(val);
	document.getElementsByTagName('body')[0].appendChild(iDiv2);

});	



let resetBtn = document.createElement("button");
resetBtn.innerHTML = "Reset";
resetBtn.style.background='#C71585';
resetBtn.style.color='#ffffff';
resetBtn.style.marginLeft="15px";
resetBtn.addEventListener("click", function () {
	f.reset();
	document.getElementsByTagName('body')[0].removeChild(document.getElementsByTagName('body')[0].lastChild);
});

var liBtn = document.createElement("li");
liBtn.appendChild(btn);
liBtn.appendChild(resetBtn);
liBtn.style.marginTop="5px";

elementful2.appendChild(liBtn);



document.getElementsByTagName('body')[0].appendChild(iDiv3);




//-------------------------------------


// YOUR CODE ENDS HERE
