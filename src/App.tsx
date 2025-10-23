import { useState } from "react";
import { HomePage } from "./components/HomePage";
import { AuthPage } from "./components/AuthPage";
import { DashboardLayout } from "./components/DashboardLayout";
import { TestsPage } from "./components/TestsPage";
import { StudentsPage } from "./components/StudentsPage";
import { GroupsPage } from "./components/GroupsPage";
import { StatisticsPage } from "./components/StatisticsPage";

type Page = "home" | "auth" | "dashboard" | "tests" | "students" | "groups" | "statistics";

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>("home");

  const handleNavigate = (page: string) => {
    setCurrentPage(page as Page);
  };

  const handleCreateTest = () => {
    // Navigate to home page for test creation
    setCurrentPage("home");
  };

  // Render different pages based on current page
  if (currentPage === "home") {
    return <HomePage onNavigate={handleNavigate} />;
  }

  if (currentPage === "auth") {
    return <AuthPage onNavigate={handleNavigate} />;
  }

  // Dashboard pages with layout
  const dashboardPages = ["dashboard", "tests", "students", "groups", "statistics"];
  if (dashboardPages.includes(currentPage)) {
    // Default to tests page if just "dashboard"
    const activePage = currentPage === "dashboard" ? "tests" : currentPage;
    
    return (
      <DashboardLayout 
        currentPage={activePage} 
        onNavigate={handleNavigate}
        onCreateTest={handleCreateTest}
      >
        {activePage === "tests" && <TestsPage />}
        {activePage === "students" && <StudentsPage />}
        {activePage === "groups" && <GroupsPage />}
        {activePage === "statistics" && <StatisticsPage />}
      </DashboardLayout>
    );
  }

  return null;
}
