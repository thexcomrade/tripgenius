import axios, { AxiosError, AxiosInstance } from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export interface AITripRequest {
  destination: string;
  duration_days: number;
  budget: number;
  travelers_count: number;
  travel_style?: string;
  interests: string[];
  transportation_mode?: string;
  preferred_accommodation?: string;
}

export interface TripCreateRequest {
  trip_title: string;
  destination: string;
  duration_days: number;
  budget: number;
  travelers_count: number;
  travel_style?: string;
  interests: string[];
  transportation_mode?: string;
  preferred_accommodation?: string;
}

export interface TripResponse {
  id: string;
  user_id: string;
  trip_title: string;
  destination: string;
  duration_days: number;
  budget: number;
  status: string;
  created_at: string;
}

class TripService {
  private readonly api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 60000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem("tripgenius_token");

      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    });
  }

  async generateAIItinerary(payload: AITripRequest): Promise<any> {
    try {
      const response = await this.api.post(
        "/api/trips/generate-ai-itinerary",
        payload,
      );

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async createTrip(payload: TripCreateRequest): Promise<TripResponse> {
    try {
      const response = await this.api.post<TripResponse>(
        "/api/trips/create",
        payload,
      );

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getTrip(tripId: string): Promise<any> {
    try {
      const response = await this.api.get(`/api/trips/${tripId}`);

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async updateTrip(tripId: string, payload: any): Promise<any> {
    try {
      const response = await this.api.put(`/api/trips/${tripId}`, payload);

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async deleteTrip(tripId: string): Promise<void> {
    try {
      await this.api.delete(`/api/trips/${tripId}`);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getHistory(): Promise<any> {
    try {
      const response = await this.api.get("/api/trips/history/list");

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async getStatistics(): Promise<any> {
    try {
      const response = await this.api.get("/api/trips/statistics/summary");

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async favoriteTrip(tripId: string): Promise<any> {
    try {
      const response = await this.api.post(`/api/trips/${tripId}/favorite`);

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async unfavoriteTrip(tripId: string): Promise<any> {
    try {
      const response = await this.api.post(`/api/trips/${tripId}/unfavorite`);

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  private handleError(error: unknown): Error {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<any>;
      const status = axiosError.response?.status;
      const detail =
        axiosError.response?.data?.detail || axiosError.response?.data?.message;

      if (status === 401) {
        return new Error("Please log in again. Your session may have expired.");
      }
      if (status === 403) {
        return new Error("You do not have permission to access this resource.");
      }
      if (status === 404) {
        return new Error("The requested trip or resource was not found.");
      }
      if (status === 422) {
        return new Error(
          `Invalid request data: ${detail || "Please check your inputs."}`,
        );
      }
      if (status === 429) {
        return new Error(
          "Too many requests. Please wait a moment and try again.",
        );
      }
      if (status && status >= 500) {
        return new Error(
          detail
            ? `Server error: ${detail}`
            : "The travel service is temporarily unavailable. Please try again.",
        );
      }
      if (!axiosError.response) {
        return new Error(
          "Unable to reach the travel service. Please check your connection or ensure the backend is running.",
        );
      }

      return new Error(detail || axiosError.message || "Request failed");
    }

    return new Error("An unexpected error occurred.");
  }
}

export const tripService = new TripService();

export default tripService;
