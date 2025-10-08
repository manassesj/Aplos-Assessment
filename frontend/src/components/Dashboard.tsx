import React, { useEffect, useState, useMemo } from "react";
import Filters from "./Filters";
import Charts from "./Charts";
import {
  getTopProducts,
  getSalesByRegion,
  getSalesByAgeGroup,
} from "../api/api";
import type { MetricRecord } from "../models/metrics";

const Dashboard: React.FC = () => {
  const [topProducts, setTopProducts] = useState<MetricRecord[]>([]);
  const [salesByRegion, setSalesByRegion] = useState<MetricRecord[]>([]);
  const [salesByAgeGroup, setSalesByAgeGroup] = useState<MetricRecord[]>([]);
  const [category, setCategory] = useState("");
  const [region, setRegion] = useState("");
  const [ageGroup, setAgeGroup] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Helper function for logging
  const log = (message: string, data?: any) => {
    console.log(`[Dashboard] ${message}`, data ?? "");
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        log("Fetching data...");
        setLoading(true);

        const [products, regionData, ageData] = await Promise.all([
          getTopProducts(),
          getSalesByRegion(),
          getSalesByAgeGroup(),
        ]);

        log("Top Products fetched", products);
        log("Sales by Region fetched", regionData);
        log("Sales by Age Group fetched", ageData);

        setTopProducts(products);
        setSalesByRegion(regionData);
        setSalesByAgeGroup(ageData);
      } catch (err) {
        console.error("[Dashboard] Error fetching data:", err);
        setError(
          err instanceof Error
            ? err.message
            : "Failed to fetch data from the API"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Filters
  const filteredTopProducts = useMemo(() => {
    if (!category) return topProducts;
    return topProducts.filter((p) =>
      (p.name ?? p.category ?? "")
        .toString()
        .toLowerCase()
        .includes(category.toLowerCase())
    );
  }, [topProducts, category]);

  const filteredSalesByRegion = useMemo(() => {
    if (!region) return salesByRegion;
    return salesByRegion.filter((r) =>
      (r.name ?? r.region ?? "").toString().toLowerCase().includes(region.toLowerCase())
    );
  }, [salesByRegion, region]);

  const filteredSalesByAgeGroup = useMemo(() => {
    if (!ageGroup) return salesByAgeGroup;
    return salesByAgeGroup.filter((a) => (a.ageGroup ?? "").toString() === ageGroup);
  }, [salesByAgeGroup, ageGroup]);

  // Format numbers as currency
  const formatCurrency = (value: number) =>
    value.toLocaleString("en-US", { style: "currency", currency: "USD" });

  // Business insights
  const insights = [
    {
      title: "Top Product",
      value: `${topProducts[0]?.name ?? topProducts[0]?.category ?? "N/A"}`,
      detail: `Revenue: ${formatCurrency(topProducts[0]?.value ?? 0)}`,
      color: "primary",
    },
    {
      title: "Top Region",
      value: `${salesByRegion[0]?.name ?? salesByRegion[0]?.region ?? "N/A"}`,
      detail: `Revenue: ${formatCurrency(salesByRegion[0]?.value ?? 0)}`,
      color: "success",
    },
    {
      title: "Most Active Age Group",
      value: `${salesByAgeGroup[0]?.ageGroup ?? "N/A"}`,
      detail: `Revenue: ${formatCurrency(salesByAgeGroup[0]?.value ?? 0)}`,
      color: "warning",
    },
  ];

  return (
    <div className="container mt-4">
      <h1 className="mb-3">Dashboard</h1>

      <Filters
        category={category}
        setCategory={setCategory}
        region={region}
        setRegion={setRegion}
        ageGroup={ageGroup}
        setAgeGroup={setAgeGroup}
      />

      {loading ? (
        <div className="alert alert-info">Loading data...</div>
      ) : error ? (
        <div className="alert alert-danger">
          <strong>Error:</strong> {error}
        </div>
      ) : (
        <>
          <Charts
            topProducts={filteredTopProducts}
            salesByRegion={filteredSalesByRegion}
            salesByAgeGroup={filteredSalesByAgeGroup}
          />

          <div className="mt-4">
            <h2>Business Insights</h2>
            <div className="row g-3">
              {insights.map((insight, idx) => (
                <div key={idx} className="col-12 col-md-4">
                  <div className={`card text-white bg-${insight.color} h-100`}>
                    <div className="card-body">
                      <h5 className="card-title">{insight.title}</h5>
                      <h6 className="card-subtitle mb-2">{insight.value}</h6>
                      <p className="card-text">{insight.detail}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
