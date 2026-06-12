import "./StatCard.css";

function StatCard({
  title,
  value,
  icon,
  growth
}) {
  return (
    <div className="stat-card">

      <div className="stat-header">

        <div className="stat-icon">
          {icon}
        </div>

        <span className="growth">
          {growth}
        </span>

      </div>

      <h2>{value}</h2>

      <p>{title}</p>

    </div>
  );
}

export default StatCard;