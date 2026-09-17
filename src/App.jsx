import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom'
import { AuthProvider, useAuth } from './features/auth/useAuth'
import Layout from './components/Layout'
import Dashboard from './features/projects/Dashboard'
import MapView from './features/map/MapView'
import SiteDetail from './features/projects/SiteDetail'
import Login from './features/auth/Login'
import Register from './features/auth/Register'

function ProtectedRoute() {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return <Outlet />
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public Authentication Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Application Routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="/map" element={<MapView />} />
              <Route path="/site/:id" element={<SiteDetail />} />
            </Route>
          </Route>

          {/* Fallback Catch-all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

