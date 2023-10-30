document.addEventListener('DOMContentLoaded', function() {
    const closeAlertBtn = document.getElementById('closeAlert');
    
    if (closeAlertBtn) {
        closeAlertBtn.addEventListener('click', function() {
            const alertRow = document.getElementById('alertRow');
            if (alertRow) {
                alertRow.remove();
            }
        });
    }
});