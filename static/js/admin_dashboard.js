document.addEventListener("DOMContentLoaded", function () {

    const deleteButtons =
        document.querySelectorAll(".delete");

    deleteButtons.forEach(button => {

        button.addEventListener("click", function (e) {

            const confirmDelete =
                confirm("Are you sure you want to delete this record?");

            if (!confirmDelete) {

                e.preventDefault();

            }

        });

    });

});


const cancelButtons =
    document.querySelectorAll(".cancel-btn");

cancelButtons.forEach(button => {

    button.addEventListener("click", function(e){

        let confirmCancel =
            confirm("Cancel this appointment?");

        if(!confirmCancel){

            e.preventDefault();

        }

    });

});

function searchTable() {

    let input =
        document.getElementById("searchInput");

    let filter =
        input.value.toUpperCase();

    let tables =
        document.querySelectorAll("table");

    tables.forEach(table => {

        let rows =
            table.getElementsByTagName("tr");

        for (let i = 1; i < rows.length; i++) {

            let text =
                rows[i].innerText.toUpperCase();

            rows[i].style.display =
                text.includes(filter)
                    ? ""
                    : "none";

        }

    });

}


function filterStatus() {

    let status =
        document.getElementById("statusFilter").value;

    let rows =
        document.querySelectorAll("#appointmentTable tr");

    rows.forEach((row, index) => {

        if (index === 0) return;

        if (status === "") {

            row.style.display = "";

        }

        else if (row.innerText.includes(status)) {

            row.style.display = "";

        }

        else {

            row.style.display = "none";

        }

    });

}