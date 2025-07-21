let user_id = localStorage.getItem("uid") || "8021650136";
const API = "http://localhost:8000"; // для локального запуска

function drawChart(data) {
  const ctx = document.getElementById("bcnChart").getContext("2d");
  if (window.bcnChart) window.bcnChart.destroy();
  window.bcnChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.dates,
      datasets: [
        {
          label: "Пополнения",
          data: data.deposits,
          borderColor: "green",
          fill: false
        },
        {
          label: "Выводы",
          data: data.withdrawals,
          borderColor: "red",
          fill: false
        }
      ]
    },
    options: { responsive: true }
  });
}

function loadStats(range = 7) {
  fetch(`${API}/api/stats/daily?range=${range}`)
    .then(res => res.json())
    .then(drawChart)
    .catch(console.error);
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("range7").onclick = () => loadStats(7);
  document.getElementById("range30").onclick = () => loadStats(30);
  document.getElementById("rangeAll").onclick = () => loadStats(365);
  loadStats();
});
