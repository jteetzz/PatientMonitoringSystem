function goToPatient(id) {
    window.location.href = `/patients/${id}`;
}

// Auto-refresh dashboard every 10 seconds
document.addEventListener("DOMContentLoaded", () => {
    const isDashboard = window.location.pathname === "/";
    if (isDashboard) {
        setInterval(() => {
            window.location.reload();
        }, 10000);
    }
});
