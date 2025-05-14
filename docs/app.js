document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("chart");
  const chartCtx = canvas.getContext("2d");
  const loadingElement = document.getElementById("loading");

  // Datos de muestra en caso de fallo
  const sampleData = [
    {"date": "2020-01-01", "deaths": 1200},
    {"date": "2020-02-01", "deaths": 1150},
    {"date": "2020-03-01", "deaths": 1300},
    {"date": "2020-04-01", "deaths": 1500},
    {"date": "2020-05-01", "deaths": 1800},
    {"date": "2020-06-01", "deaths": 2100},
    {"date": "2020-07-01", "deaths": 2300},
    {"date": "2020-08-01", "deaths": 2100},
    {"date": "2020-09-01", "deaths": 1900},
    {"date": "2020-10-01", "deaths": 1700},
    {"date": "2020-11-01", "deaths": 1600},
    {"date": "2020-12-01", "deaths": 1500}
  ];

  // Ruta al archivo JSON en el sitio publicado
  const dataPath = "data/muertes_mx_clean.json";

  // Función para cargar los datos
  async function loadData() {
    try {
      const response = await fetch(dataPath);
      if (response.ok) {
        return await response.json();
      } else {
        console.warn(`No se pudo cargar los datos desde ${dataPath}, usando datos de muestra.`);
        return sampleData;
      }
    } catch (error) {
      console.error(`Error al cargar los datos: ${error}`);
      return sampleData;
    }
  }

  // Procesar los datos para la visualización
  function processData(data) {
    const dates = data.map(item => item.date);
    const deaths = data.map(item => parseInt(item.deaths, 10));

    return {
      dates: dates,
      deaths: deaths,
    };
  }

  // Crear la gráfica con Chart.js
  function createChart(data, ctx) {
    const color = "rgba(0, 77, 152, 0.8)";

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
            fill: false
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
              label: function (context) {
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

  // Cargar los datos e inicializar la gráfica
  loadData()
    .then(data => {
      const chartData = processData(data);
      if (loadingElement) {
        loadingElement.style.display = "none";
      }
      canvas.style.display = "block";
      createChart(chartData, chartCtx);
    })
    .catch(error => {
      console.error("Error en el proceso completo:", error);
      if (loadingElement) {
        loadingElement.innerHTML = `
          <div class="error-message">
            <h3>Error al cargar los datos</h3>
            <p>${error.message}</p>
            <p>Se han intentado todas las rutas posibles.</p>
          </div>`;
      }
    });
});
