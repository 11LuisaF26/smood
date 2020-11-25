
function CompareDate() {
    var FinishDate = document.getElementById("fecha_final_red_social").value;
    var StartDate = document.getElementById("fecha_inicio_red_social").value;

    if (new Date(FinishDate).getTime() <= new Date(StartDate).getTime()) {
        alert("La fecha final de la escucha debe ser mayor y diferente a la fecha de inicio");
        document.getElementById("fecha_final_red_social").value="";
        document.getElementById("fecha_inicio_red_social").value = "";
        return false;
    }
    return true;
}