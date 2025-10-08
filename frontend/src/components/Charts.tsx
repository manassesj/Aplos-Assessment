import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import type { MetricRecord } from "../models/metrics";

interface ChartsProps {
  topProducts: MetricRecord[];
  salesByRegion: MetricRecord[];
  salesByAgeGroup: MetricRecord[];
}

const Charts: React.FC<ChartsProps> = ({ topProducts, salesByRegion, salesByAgeGroup }) => {
  return (
    <div className="row g-4">
      <div className="col-12 col-md-4">
        <h5 className="text-center mb-2">Top Products</h5>
        <div className="border p-2">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topProducts}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="col-12 col-md-4">
        <h5 className="text-center mb-2">Sales by Region</h5>
        <div className="border p-2">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salesByRegion}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="col-12 col-md-4">
        <h5 className="text-center mb-2">Revenue by Age Group</h5>
        <div className="border p-2">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salesByAgeGroup}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#ffc658" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Charts;
