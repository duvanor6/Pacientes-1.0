function validar_formulario(){
    let userId= document.getElementById("iduser");
    let clave= document.getElementById("idpwd");
    let correo= document.getElementById("idcorreo");
    console.log(userId);
    // Validacion del User
    if (userId.value.length==0 || userId.value.length<8){
        alert("Debes ingresar un Username con min. 8 caracteres");
        userId.focus();
    }
    // Validacion del password
    if (clave.value.length==0 || clave.value.length<8){
        alert("Debes ingresar un Password con min. 8 caracteres");
        clave.focus();
    }
    // Validacion del correo
    email_checked();
}
function email_checked(){
    let flag= true;
    let correo= document.getElementById("idcorreo");
    let indice = correo.value.indexOf("@");
    if (indice==-1){
        flag= false; 
    } else {
        let myArr= correo.value.split("@");
        if (myArr[0].length<2 || myArr[1].indexOf(".")==-1) {
            flag= false;
        }
    }
    if (!flag) {
        alert("El correo no tiene la forma correcta xxx@yyy.zzz");
        correo.focus();
    } 
}
function mostrarPassword(obj) {
    var obj = document.getElementById("idpwd");
    obj.type = "text";
  }
  function ocultarPassword(obj) {
    var obj = document.getElementById("idpwd");
    obj.type = "password";
  }