var band1=0;
var band2=0;
var band3=0;
var mult=1e0;
var tolerance=0;




function myvalue(element,col,row){
    // setting bands value
    if(element.innerHTML!="&nbsp;"){
        if(col==1){
            band1=row;
        }else if(col==2){
            band2=row;
        }else if(col==3){
            mult=row;
        }else{
            tolerance=row;
        }

        var result=document.getElementById('value');
// result.innerHTML="Band1: "+band1+"  Band2:"+band2+"  Multi.: "+mult;
   // reset borders
        for(r=0;r<=10;r++){
            var targetF=document.getElementById("c"+col+"r"+r);
                targetF.style.border="1px solid black";
            }

        element.style.border="1px solid white";
        myRgbColor=element.style.backgroundColor;
        targetE=  document.getElementById("resb"+String(col));
        targetE.style.fill=myRgbColor;
        result.innerHTML=resultString();
    }
    
}

function resultString(){
    return getOhmsString(calculteResistance())+' ±' + tolerance*100 + '%';
}

function getOhmsString(ohms){
    var suffix = 'Ω'
    if (ohms/1e6 >= 1) {
      suffix = 'MΩ';
      ohms = ohms/1e6;
    }else if (ohms/1e3 >= 1) {
      suffix = 'KΩ';
      ohms = ohms/1e3;
    }
    return ohms + suffix;
}

function calculteResistance(){
    var ohms = (band1*10 + band2) * mult;
      return ohms;
}

function toleranceLevel(){
    return tolerance*100;
}

function showAbout(){
    Android.showAbout();
}