document.addEventListener("DOMContentLoaded", function() {
    const btnDelete = document.querySelectorAll('.btn-delete');
    if (btnDelete) {
        const btnDeleteArray = Array.from(btnDelete);
        btnDeleteArray.forEach((btn) => {
            btn.addEventListener('click', (e) => {
                if (!confirm('¿Está seguro de eliminar el elemento?')) {
                    e.preventDefault();
                }
            });
        });
    }
});


