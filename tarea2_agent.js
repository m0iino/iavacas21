function reflex_agent(location, state){
  console.log("")
    if (state=="DIRTY") return "CLEAN";
    else if (location=="A") return "RIGHT";
    else if (location=="B") return "LEFT";
}
var count = 0;
var count2 = 0;
function test(states){
      count = count + 1;
      count2 = count2 + 1;
      //console.log(count);
       var location = states[0];		
       var state = states[0] == "A" ? states[1] : states[2];
       var action_result = reflex_agent(location, state);
       document.getElementById("log").innerHTML+="<br>Location: ".concat(location).concat(" | Action: ").concat(action_result);
       if (action_result == "CLEAN"){
         
         if (location == "A") states[1] = "CLEAN";
          else if (location == "B") states[2] = "CLEAN";
        
       }
       else if (action_result == "RIGHT" && states[1] == "CLEAN" && states[2] == "CLEAN" && count == 5 ){
        
        states = ["B","DIRTY","DIRTY"];
        count = 0;
        
        
      }
      else if (action_result == "LEFT" && states[1] == "CLEAN" && states[2] == "CLEAN" && count == 5 ){
        states = ["A","DIRTY","DIRTY"];
        count = 0;
      }
       else if (action_result == "RIGHT"){
        states[0] = "B";
        
       } 
       else if (action_result == "LEFT"){
        states[0] = "A";	
        	
       } 
       if(count2 == 8){
        
      }else {
        setTimeout(function(){ test(states); }, 2000);
      }
}

var states = ["A","DIRTY","DIRTY"];

test(states);  
