document.addEventListener("DOMContentLoaded", function () {
  const chartCtx = document.getElementById("chart").getContext("2d");

  // Cargar datos desde el archivo JSON
  fetch("data/muertes_mx_clean.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error(¡Error HTTP! Estado: ${response.status});
      }
      return response.json();
    })
    .then((data) => {
      // Procesar los datos para la visualización
      return processData(data);
    })
    .then((chartData) => {
      createChart(chartData, chartCtx);
    })
    .catch((error) => {
      console.error("Error cargando datos:", error);
      document.querySelector(
        ".chart-container"
      ).innerHTML = `<div class="error-message">
          <h3>Error al cargar los datos</h3>
          <p>${error.message}</p>
          <p>Ruta intentada: data/muertes_mx_clean.json</p>
        </div>`;
    });
});

function processData(data) {
  // Limpiar y verificar los datos
  const dates = [];
  const muertes = [];

  data.forEach((item) => {
    const date = item.date; // Ajustar la columna de fecha
    const muertesValue = parseInt(item.deaths, 10); // Ajustar la columna de muertes

    if (date && !isNaN(muertesValue)) {
      dates.push(date);
      muertes.push(muertesValue);
    }
  });

  return {
    dates: dates,
    muertes: muertes,
  };
}

function createChart(data, ctx) {
  const color = "rgba(0, 77, 152, 0.8)"; // Color para muertes

  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.dates,
      datasets: [
        {
          label: "Muertes",
          data: data.muertes,
          backgroundColor: color,
          borderColor: color.replace("0.8", "1"),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Número de Muertes en México",
          font: {
            size: 18,
            weight: "bold",
          },
          padding: {
            top: 10,
            bottom: 20,
          },
        },
        legend: {
          position: "top",
        },
        tooltip: {
          callbacks: {
            afterLabel: function (context) {
              const index = context.dataIndex;
              return Muertes: ${data.muertes[index]};
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Número de Muertes",
          },
          grid: {
            display: true,
            color: "rgba(0, 0, 0, 0.05)",
          },
        },
        x: {
          title: {
            display: true,
            text: "Fecha",
          },
          grid: {
            display: false,
          },
        },
      },
    },
  });
}