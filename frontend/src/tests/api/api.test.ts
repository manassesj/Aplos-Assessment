import axios from "axios";
import  {
  getTopProducts,
  getSalesByRegion,
  getSalesByAgeGroup,
} from "../../api/api";

jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("API functions", () => {
  it("fetches top products", async () => {
    const mockData = [{ category: "Home", revenue: 100 }];
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    const data = await getTopProducts();
    expect(data).toEqual([{ name: "Home", value: 100 }]);
    expect(mockedAxios.get).toHaveBeenCalledWith("/top-products");
  });

  it("fetches sales by region", async () => {
    const mockData = [{ region: "East", revenue: 200 }];
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    const data = await getSalesByRegion();
    expect(data).toEqual([{ name: "East", value: 200 }]);
    expect(mockedAxios.get).toHaveBeenCalledWith("/sales-by-region");
  });

  it("fetches sales by age group", async () => {
    const mockData = [{ age_group: "<25", revenue: 300 }];
    mockedAxios.get.mockResolvedValueOnce({ data: mockData });

    const data = await getSalesByAgeGroup();
    expect(data).toEqual([{ name: "<25", value: 300 }]);
    expect(mockedAxios.get).toHaveBeenCalledWith("/sales-by-age-group");
  });

  it("handles API errors", async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error("Network Error"));
    await expect(getTopProducts()).rejects.toThrow("Network Error");
  });
});
