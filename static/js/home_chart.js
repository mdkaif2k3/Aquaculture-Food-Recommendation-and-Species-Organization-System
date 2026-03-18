document.addEventListener("DOMContentLoaded", () => {
  const makeChart = (id, labelsId, dataId, type, showLegend = false) => {
    const el = document.getElementById(id);
    if (!el) return;

    const labels = JSON.parse(document.getElementById(labelsId).textContent);
    const data = JSON.parse(document.getElementById(dataId).textContent);

    new Chart(el.getContext("2d"), {
      type,
      data: {
        labels,
        datasets: [{
          data,
          backgroundColor: [
            "rgba(46, 199, 255,.7)",
            "rgba(0, 187, 255,.7)",
            "rgba(0, 153, 209,.7)",
            "rgba(0, 120, 163,.7)"
          ]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: showLegend, position: "bottom" },
            tooltip: {
                enabled: true,
                callbacks: {
                    label: function (context) {
                    const data = context.dataset.data;

                    // SAFETY CHECK
                    if (!data || !data.length) return "";

                    const total = data.reduce((sum, val) => sum + val, 0);
                    const value = context.raw;
                    const percent = ((value / total) * 100).toFixed(1);

                    return `${percent}%`;
                    }
                }
            }
        }
      }
    });
  };

  makeChart("watertypeChart", "water-labels", "water-data", "bar");
  makeChart("habitatChart", "habitat-labels", "habitat-data", "pie", true);
  makeChart("threatenedChart", "threat-labels", "threat-data", "doughnut", true);
});