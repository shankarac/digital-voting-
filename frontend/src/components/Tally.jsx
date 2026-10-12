import { percent } from "../format";

const ROWS = [
  ["yes", "Yes"],
  ["no", "No"],
  ["abstain", "Abstain"],
];

export function Tally({ proposal }) {
  const total = proposal.total_votes || 0;
  return (
    <div className="tally" aria-label="Vote counts">
      {ROWS.map(([key, label]) => {
        const count = proposal[`${key}_count`] || 0;
        const share = percent(count, total);
        return (
          <div className="tally-row" key={key}>
            <span>{label}</span>
            <span className="bar" aria-hidden="true">
              <span className={key} style={{ width: `${share}%` }} />
            </span>
            <span className="count">
              {count}
              {total ? ` · ${share}%` : ""}
            </span>
          </div>
        );
      })}
    </div>
  );
}
