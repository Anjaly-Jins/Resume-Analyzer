const input = document.getElementById("resume");

const fileName = document.getElementById("filename");

input.addEventListener("change", function(){

if(this.files.length>0){

fileName.innerHTML=this.files[0].name;

}

});