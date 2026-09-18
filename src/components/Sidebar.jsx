import { NavLink } from "react-router-dom";
import { LayoutDashboard, Map, LogOut, User } from "lucide-react";
import { useAuth } from "../features/auth/useAuth";

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/map", label: "Map", icon: Map },
];

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="flex flex-col w-56 shrink-0 bg-forest h-full">
      {/* Brand mark */}
      <div className="px-5 py-6 border-b border-forest-light">
        <span className="text-cream font-semibold text-lg tracking-tight">
          Darukaa<span className="text-amber">.</span>Earth
        </span>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? "bg-forest-light text-cream"
                  : "text-cream/60 hover:bg-forest-light/50 hover:text-cream"
              }`
            }
          >
            <Icon size={16} strokeWidth={1.75} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="p-3 border-t border-forest-light space-y-2">
        {user?.email && (
          <div className="flex items-center gap-2 px-2 py-1 text-cream/70 text-xs truncate">
            <User size={13} className="shrink-0 text-amber" />
            <span className="truncate">{user.email}</span>
          </div>
        )}
        <button
          onClick={logout}
          className="w-full flex items-center gap-2.5 px-3 py-1.5 rounded-md text-xs font-medium text-cream/60 hover:bg-forest-light/50 hover:text-amber transition-colors"
        >
          <LogOut size={14} />
          Sign out
        </button>
        <p className="text-cream/30 text-[10px] px-2">v0.1.0-alpha</p>
      </div>
    </aside>
  );
}
