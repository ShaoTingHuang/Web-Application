var new_val = 0; var prev_val = 0; var prev_op = "+"; var flag = true;
function plus(){
  compute();
  prev_op = "+";
  document.getElementById("display").value = prev_val;
}
function minus(){
  compute();
  prev_op = "-";
  document.getElementById("display").value = prev_val;
}
function times(){
  compute();
  prev_op = "*";
  document.getElementById("display").value = prev_val;
}
function divides(){
  compute();
  prev_op = "/";
  document.getElementById("display").value = prev_val;
}
function equals(){
  compute();
  document.getElementById("display").value = prev_val;
  new_val = 0;
  prev_op = "+";
}
function compute(){
  switch(prev_op) {
		case "+":
      if (prev_val != 0) {
        prev_val = parseInt(prev_val) + parseInt(new_val);
      } else {
        prev_val = new_val;
      }
      new_val = 0;
			break;
		case "-":
      if (prev_val != 0) {
        prev_val = parseInt(prev_val) - parseInt(new_val);
      } else {
        prev_val = new_val;
      }
      new_val = 0;
			break;
		case "*":
      if (prev_val != 0) {
        if (flag == true) {
          prev_val = parseInt(prev_val) * parseInt(new_val);
          flag == false;
        }
      } else {
        prev_val = new_val;
      }
      new_val = 0;
      break;
		case "/":
      if (prev_val != 0) {
        prev_val = parseInt(prev_val) / parseInt(new_val);
      } else {
        prev_val = new_val;
      }
      new_val = 0;
			break;
	}
}

function displays(num){
  new_val *= 10;
  new_val += parseInt(num);
  document.getElementById("display").value = new_val;
}
