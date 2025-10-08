import React from "react";

interface FiltersProps {
  category: string;
  region: string;
  ageGroup: string;
  setCategory: (value: string) => void;
  setRegion: (value: string) => void;
  setAgeGroup: (value: string) => void;
}

const ageGroups = ["<25", "25-34", "35-44", "45-54", "55+"];

const Filters: React.FC<FiltersProps> = ({
  category,
  region,
  ageGroup,
  setCategory,
  setRegion,
  setAgeGroup
}) => {
  return (
    <div className="d-flex flex-wrap gap-3 mb-4">
      <div className="flex-grow-1">
        <label className="form-label">Filter by Category (Top Products)</label>
        <input
          type="text"
          placeholder="Enter category"
          value={category}
          onChange={e => setCategory(e.target.value)}
          className="form-control"
        />
      </div>

      <div className="flex-grow-1">
        <label className="form-label">Filter by Region (Sales by Region)</label>
        <input
          type="text"
          placeholder="Enter region"
          value={region}
          onChange={e => setRegion(e.target.value)}
          className="form-control"
        />
      </div>

      <div className="flex-grow-1">
        <label className="form-label">Filter by Age Group (Sales by Age Group)</label>
        <select
          value={ageGroup}
          onChange={e => setAgeGroup(e.target.value)}
          className="form-control"
        >
          <option value="">All</option>
          {ageGroups.map(ag => (
            <option key={ag} value={ag}>{ag}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default Filters;
