document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("resumen").addEventListener("click", function () {


        const tabla = document.getElementById("tabla_resumen");

        // Crear un objeto WorkBook de SheetJS
        const wb = XLSX.utils.table_to_book(tabla);

        // Guardar el libro como un archivo de Excel
        XLSX.writeFile(wb, "tblresumen.xlsx");

    });

    document.getElementById("ventasexcel").addEventListener("click", function () {


        const tabla = document.getElementById("tabla_ventas");

        // Crear un objeto WorkBook de SheetJS
        const wb = XLSX.utils.table_to_book(tabla);

        // Guardar el libro como un archivo de Excel
        XLSX.writeFile(wb, "tblventas.xlsx");

    });
});