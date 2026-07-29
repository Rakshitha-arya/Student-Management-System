// Client-side Interactivity Script

document.addEventListener('DOMContentLoaded', function () {
    
    // Auto-dismiss alert notifications after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Delete Confirmation Modal Setup
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const studentId = button.getAttribute('data-student-id');
            const studentName = button.getAttribute('data-student-name');
            const studentUsn = button.getAttribute('data-student-usn');
            const deleteUrl = button.getAttribute('data-delete-url');

            const modalStudentName = deleteModal.querySelector('#modalStudentName');
            const modalStudentUsn = deleteModal.querySelector('#modalStudentUsn');
            const deleteForm = deleteModal.querySelector('#deleteStudentForm');

            if (modalStudentName) modalStudentName.textContent = studentName;
            if (modalStudentUsn) modalStudentUsn.textContent = studentUsn;
            if (deleteForm) deleteForm.setAttribute('action', deleteUrl);
        });
    }

    // Dynamic Image File Previewer
    const photoInput = document.getElementById('photo');
    const photoPreview = document.getElementById('photoPreview');

    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    photoPreview.setAttribute('src', e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
