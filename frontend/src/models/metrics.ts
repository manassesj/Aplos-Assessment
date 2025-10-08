export interface MetricRecord {
  name: string;      
  value: number;     
  metricType: 'topProducts' | 'salesByRegion' | 'customerDemographics';
  category?: string; 
  region?: string;   
  ageGroup?: string; 
}
