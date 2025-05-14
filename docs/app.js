document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("chart");  // Obtener el canvas por su id
  const chartCtx = canvas.getContext("2d"); // Obtener el contexto del canvas

  // Cargar datos desde el archivo JSON
  fetch("data/muertes_mx_clean.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`¡Error HTTP! Estado: ${response.status}`);
      }
      return response.json(); // Usar .json() en lugar de .text()
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
  // Extraer las fechas y los valores de muertes
  const dates = data.map((item) => item.date); // Asegúrate de que 'date' esté bien formateado en el JSON
  const deaths = data.map((item) => parseInt(item.deaths, 10));

  return {
    dates: dates,
    deaths: deaths,
  };
}

function createChart(data, ctx) {
  const color = "rgba(0, 77, 152, 0.8)"; // Color para el número de muertes

  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.dates,
      datasets: [
        {
          label: "Muertes",
          data: data.deaths,
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
              return `Muertes: ${data.deaths[index]}`;
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
