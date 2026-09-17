import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

/**
 * Wraps every page with the persistent sidebar on the left and the main
 * content area on the right. The Outlet renders the matched child route.
 */
export default function Layout() {
  return (
    <div className="flex h-full">
      <Sidebar />
      <main className="flex-1 overflow-hidden bg-cream">
        <Outlet />
      </main>
    </div>
  );
}
