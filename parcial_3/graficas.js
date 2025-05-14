// Generamos gráficos para el informe de balanceo de carga
import React, { useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export default function LoadBalancingCharts() {
  const [activeChart, setActiveChart] = useState('availability');
  
  // Datos de disponibilidad vs concurrencia
  const availabilityData = [
    { name: '25 Usuarios', disponibilidad: 100.00 },
    { name: '50 Usuarios', disponibilidad: 13.82 },
    { name: '75 Usuarios', disponibilidad: 43.63 }
  ];
  
  // Datos de transacciones exitosas vs fallidas
  const transactionsData = [
    { name: '25 Usuarios', exitosas: 1954, fallidas: 0, total: 1954 },
    { name: '50 Usuarios', exitosas: 172, fallidas: 1073, total: 1245 },
    { name: '75 Usuarios', exitosas: 850, fallidas: 1098, total: 1948 }
  ];
  
  // Datos de tiempo de respuesta vs concurrencia
  const responseTimeData = [
    { name: '25 Usuarios', tiempo: 0.23 },
    { name: '50 Usuarios', tiempo: 4.48 },
    { name: '75 Usuarios', tiempo: 1.42 }
  ];
  
  // Datos de ApacheBench para comparación
  const abData = [
    { name: 'Concurrencia 30', solicitudes: 300, tiempo: 6.52, rps: 46.05, fallos: 0 },
    { name: 'Concurrencia 40', solicitudes: 1331, tiempo: 30.01, rps: 44.36, fallos: 0 }
  ];
  
  return (
    <div className="flex flex-col gap-8 p-4 bg-gray-50 rounded-lg">
      <div className="flex justify-center space-x-4">
        <button 
          className={`px-4 py-2 rounded ${activeChart === 'availability' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveChart('availability')}
        >
          Disponibilidad
        </button>
        <button 
          className={`px-4 py-2 rounded ${activeChart === 'transactions' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveChart('transactions')}
        >
          Transacciones
        </button>
        <button 
          className={`px-4 py-2 rounded ${activeChart === 'responseTime' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveChart('responseTime')}
        >
          Tiempo de Respuesta
        </button>
        <button 
          className={`px-4 py-2 rounded ${activeChart === 'comparison' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setActiveChart('comparison')}
        >
          Comparación AB
        </button>
      </div>
      
      <div className="h-96 bg-white p-4 rounded shadow">
        {activeChart === 'availability' && (
          <div className="h-full">
            <h3 className="text-lg font-semibold text-center mb-4">Disponibilidad vs Concurrencia</h3>
            <ResponsiveContainer width="100%" height="90%">
              <BarChart
                data={availabilityData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} label={{ value: 'Disponibilidad (%)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="disponibilidad" fill="#8884d8" name="Disponibilidad (%)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
        
        {activeChart === 'transactions' && (
          <div className="h-full">
            <h3 className="text-lg font-semibold text-center mb-4">Transacciones Exitosas vs Fallidas</h3>
            <ResponsiveContainer width="100%" height="90%">
              <BarChart
                data={transactionsData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis label={{ value: 'Cantidad de Transacciones', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="exitosas" stackId="a" fill="#00C49F" name="Exitosas" />
                <Bar dataKey="fallidas" stackId="a" fill="#FF8042" name="Fallidas" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
        
        {activeChart === 'responseTime' && (
          <div className="h-full">
            <h3 className="text-lg font-semibold text-center mb-4">Tiempo de Respuesta vs Concurrencia</h3>
            <ResponsiveContainer width="100%" height="90%">
              <LineChart
                data={responseTimeData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis label={{ value: 'Tiempo de Respuesta (s)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="tiempo" stroke="#8884d8" activeDot={{ r: 8 }} name="Tiempo de Respuesta (s)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
        
        {activeChart === 'comparison' && (
          <div className="h-full">
            <h3 className="text-lg font-semibold text-center mb-4">Comparación de Pruebas ApacheBench</h3>
            <ResponsiveContainer width="100%" height="90%">
              <BarChart
                data={abData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="solicitudes" fill="#8884d8" name="Solicitudes Totales" />
                <Bar dataKey="rps" fill="#82ca9d" name="Solicitudes por Segundo" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
      
      <div className="bg-white p-4 rounded shadow">
        <h3 className="text-lg font-semibold mb-2">Resumen de Hallazgos</h3>
        <ul className="list-disc pl-5 space-y-1">
          <li>El servidor muestra un rendimiento óptimo hasta 25 usuarios concurrentes con 100% de disponibilidad.</li>
          <li>Entre 25-50 usuarios se alcanza un punto crítico donde la disponibilidad cae al 13.82%.</li>
          <li>El tiempo de respuesta aumenta de 0.23s a 4.48s al pasar de 25 a 50 usuarios.</li>
          <li>Curiosamente, con 75 usuarios algunas métricas mejoran en comparación con 50 usuarios.</li>
          <li>Se recomienda implementar balanceo de carga para mantener una concurrencia por servidor no mayor a 25 usuarios.</li>
        </ul>
      </div>
    </div>
  );
}