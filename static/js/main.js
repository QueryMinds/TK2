console.log('Script is loaded');

function updateFormState() {
    console.log('updateFormState called'); 
    var category = document.getElementById("category").value;
    console.log('hi2');

    // Sembunyikan semua div terlebih dahulu
    document.getElementById("topupFields").style.display = "none";
    document.getElementById("jasaFields").style.display = "none";
    document.getElementById("transferFields").style.display = "none";
    document.getElementById("withdrawFields").style.display = "none";

    // Tampilkan form sesuai kategori
    if (category == "topup") {
        document.getElementById("topupFields").style.display = "block";
    } else if (category == "jasa") {
        document.getElementById("jasaFields").style.display = "block";
    } else if (category == "transfer") {
        document.getElementById("transferFields").style.display = "block";
    } else if (category == "withdrawal") {
        document.getElementById("withdrawFields").style.display = "block";
    }
}

window.onload = function () {
    console.log('Window Loaded');
    updateFormState();
};
