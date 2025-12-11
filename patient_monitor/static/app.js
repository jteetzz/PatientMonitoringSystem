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

document.addEventListener("DOMContentLoaded", () => {
    const filterButtons = document.querySelectorAll(".alert-filters .chip");
    const alerts = document.querySelectorAll(".alert-item");

    if (!filterButtons.length || !alerts.length) return;

    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const filter = btn.getAttribute("data-filter");

            // toggle active chip style
            filterButtons.forEach(b => b.classList.remove("chip-active"));
            btn.classList.add("chip-active");

            alerts.forEach(alert => {
                const isCritical = alert.classList.contains("alert-critical");
                const isWarning  = alert.classList.contains("alert-warning");
                const isInfo     = alert.classList.contains("alert-info");

                let show = false;
                if (filter === "all") show = true;
                else if (filter === "critical") show = isCritical;
                else if (filter === "warning") show = isWarning;
                alert.style.display = show ? "block" : "none";
            });
        });
    });
});

