import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from 'recharts'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

const monthlyApplications = [
  { month: 'Jan', approved: 72 },
  { month: 'Feb', approved: 68 },
  { month: 'Mar', approved: 79 },
  { month: 'Apr', approved: 83 },
  { month: 'May', approved: 88 },
]

const riskBands = [
  { band: 'Low', count: 54 },
  { band: 'Medium', count: 31 },
  { band: 'High', count: 15 },
]

function App() {
  return (
    <BrowserRouter>
      <div className="mx-auto min-h-screen w-full max-w-6xl p-4 md:p-8">
        <header className="mb-8 rounded-2xl border border-slate-200 bg-white/80 p-5 shadow-sm backdrop-blur md:p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-700">Cognizant Hackathon 2025</p>
          <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900 md:text-4xl">LoanSense AI</h1>
          <p className="mt-2 text-slate-600">AI-Powered Loan Eligibility & Risk Assessment System</p>
          <nav className="mt-4 flex gap-3 text-sm font-medium">
            <NavItem to="/">Overview</NavItem>
            <NavItem to="/insights">Risk Insights</NavItem>
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/insights" element={<InsightsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

function NavItem({ to, children }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `rounded-full px-4 py-2 transition ${
          isActive ? 'bg-cyan-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
        }`
      }
    >
      {children}
    </NavLink>
  )
}

function OverviewPage() {
  const [backendStatus, setBackendStatus] = useState('Checking backend...')

  useEffect(() => {
    // Friendly example of calling FastAPI from React using Axios.
    const checkHealth = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/health')
        setBackendStatus(`Backend is online: ${response.data.status}`)
      } catch {
        setBackendStatus('Backend not reachable yet. Start FastAPI server to enable live checks.')
      }
    }

    checkHealth()
  }, [])

  const lineData = useMemo(
    () => ({
      labels: monthlyApplications.map((item) => item.month),
      datasets: [
        {
          label: 'Approval Rate (%)',
          data: monthlyApplications.map((item) => item.approved),
          borderColor: '#0f766e',
          backgroundColor: 'rgba(15, 118, 110, 0.2)',
          tension: 0.25,
        },
      ],
    }),
    [],
  )

  return (
    <section className="grid gap-4 md:grid-cols-2">
      <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-xl font-bold text-slate-900">System Snapshot</h2>
        <p className="mt-2 text-slate-600">
          This starter page uses React Router, Axios, and chart libraries so your hackathon team can directly start building
          loan eligibility features.
        </p>
        <p className="mt-4 rounded-lg bg-cyan-50 p-3 text-sm font-medium text-cyan-900">{backendStatus}</p>
      </article>

      <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-xl font-bold text-slate-900">Approval Trend (Chart.js)</h2>
        <div className="mt-3 h-56">
          <Line data={lineData} options={{ maintainAspectRatio: false, responsive: true }} />
        </div>
      </article>
    </section>
  )
}

function InsightsPage() {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-xl font-bold text-slate-900">Risk Distribution (Recharts)</h2>
      <p className="mt-2 text-slate-600">Simple mock data to demonstrate how risk buckets can be visualized for lending analysts.</p>
      <div className="mt-5 h-64 w-full">
        <ResponsiveContainer>
          <BarChart data={riskBands}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="band" />
            <YAxis allowDecimals={false} />
            <Bar dataKey="count" fill="#ea580c" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

function NotFoundPage() {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 text-slate-700 shadow-sm">
      <h2 className="text-xl font-bold text-slate-900">Page Not Found</h2>
      <p className="mt-2">Use the navigation above to return to your LoanSense AI dashboard pages.</p>
    </section>
  )
}

export default App
