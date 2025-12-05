/* ============================
   UTILITY: Animate Counters
============================ */
function animateCounter(id, target) {
    let count = 0;
    const el = document.getElementById(id);
    const step = Math.ceil(target / 100);
    const interval = setInterval(() => {
        count += step;
        if (count >= target) {
            count = target;
            clearInterval(interval);
        }
        el.innerText = count;
    }, 10);
}

/* ============================
   TIMELINE CHART
============================ */
fetch("/reports/timeline/")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("timelineChart"), {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Total Goals Over Time",
                    data: data.values,
                    borderColor: "#16a34a",
                    backgroundColor: "rgba(22,163,74,0.2)",
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointBackgroundColor: "#14532d",
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        enabled: true,
                        backgroundColor: '#16a34a',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        padding: 8,
                    },
                    legend: { display: false }
                },
                scales: {
                    x: { title: { display: true, text: 'Date' } },
                    y: { title: { display: true, text: 'Total Goals' }, beginAtZero: true }
                }
            }
        });
    });

/* ============================
   STATUS CHART
============================ */
fetch("/reports/status/")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("statusChart"), {
            type: "pie",
            data: {
                labels: data.map(item => item.status),
                datasets: [{
                    data: data.map(item => item.total),
                    backgroundColor: ["#16a34a", "#facc15", "#ef4444"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        enabled: true,
                        backgroundColor: '#16a34a',
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    },
                    legend: { position: 'bottom' }
                }
            }
        });
    });

/* ============================
   CATEGORY CHART
============================ */
fetch("/reports/categories/")
    .then(res => res.json())
    .then(data => {
        new Chart(document.getElementById("categoryChart"), {
            type: "bar",
            data: {
                labels: data.map(item => item.category),
                datasets: [{
                    label: "Goals per Category",
                    data: data.map(item => item.total),
                    backgroundColor: "#16a34a"
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        enabled: true,
                        backgroundColor: '#16a34a',
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    },
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    });

/* ============================
   COMPLETION SUMMARY
============================ */
fetch("/reports/completions/")
    .then(res => res.json())
    .then(data => {
        animateCounter("completedCount", data.completed);
        animateCounter("pendingCount", data.pending);

        new Chart(document.getElementById("completionChart"), {
            type: "doughnut",
            data: {
                labels: ["Completed", "Pending"],
                datasets: [{
                    data: [data.completed, data.pending],
                    backgroundColor: ["#16a34a", "#e5e7eb"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        enabled: true,
                        backgroundColor: '#16a34a',
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    },
                    legend: { position: 'bottom' }
                }
            }
        });
    });
