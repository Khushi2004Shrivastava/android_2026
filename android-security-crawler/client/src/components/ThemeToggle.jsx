export default function ThemeToggle() {
  const toggleTheme = () => {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";

    html.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  };

  return (
    <button className="theme-toggle" onClick={toggleTheme}>
      🌗 Theme
    </button>
  );
}
